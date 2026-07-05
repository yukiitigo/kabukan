import httpx
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/search")
async def search(q: str = Query(...)):
    try:
        results = []
        async with httpx.AsyncClient(timeout=10) as c:
            for lang in ["ja-JP", "en-US"]:
                r = await c.get("https://query1.finance.yahoo.com/v1/finance/search",
                    params={"q": q, "lang": lang, "region": "JP", "quotesCount": 10},
                    headers={"User-Agent": "Mozilla/5.0"})
                data = r.json()
                for item in data.get("quotes", []):
                    symbol = item.get("symbol", "")
                    if symbol.endswith(".T"):
                        code = symbol.replace(".T", "")
                        name = item.get("longname") or item.get("shortname") or code
                        if not any(x["code"] == code for x in results):
                            results.append({"code": code, "name": name})
                if results:
                    break
        return JSONResponse(content={"results": results[:10]}, media_type="application/json; charset=utf-8")
    except Exception as e:
        return JSONResponse(content={"results": [], "error": str(e)})

@app.get("/quotes")
async def quotes(codes: str = Query(...)):
    cl = [c.strip() for c in codes.split(",") if c.strip()]
    out = []
    for code in cl:
        try:
            async with httpx.AsyncClient(timeout=15, follow_redirects=True) as c:
                r = await c.get(
                    f"https://query2.finance.yahoo.com/v8/finance/chart/{code}.T",
                    params={"interval": "1d", "range": "5d"},
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36", "Accept": "application/json"})
                data = r.json()
                result = data["chart"]["result"][0]
                meta = result["meta"]
                price = meta.get("regularMarketPrice")
                prev = meta.get("chartPreviousClose")
                name = meta.get("longName") or meta.get("shortName") or code
                vol = meta.get("regularMarketVolume")
                change = round(price - prev, 1) if price and prev else None
                pct = round((price - prev) / prev * 100, 2) if price and prev else None
                out.append({"code": code, "name": name, "price": price, "prevClose": prev, "change": change, "changePct": pct, "volume": vol})
        except Exception as e:
            out.append({"code": code, "error": str(e)})
    return JSONResponse(content={"quotes": out}, media_type="application/json; charset=utf-8")

@app.get("/history/{code}")
async def history(code: str):
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as c:
            r = await c.get(
                f"https://query2.finance.yahoo.com/v8/finance/chart/{code}.T",
                params={"interval": "1d", "range": "1mo"},
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36", "Accept": "application/json"})
            data = r.json()
            result = data["chart"]["result"][0]
            ts = result["timestamp"]
            closes = result["indicators"]["quote"][0]["close"]
            from datetime import datetime
            dates = [datetime.fromtimestamp(t).strftime("%Y-%m-%d") for t in ts]
            prices = [round(float(p), 1) if p else None for p in closes]
            return JSONResponse(content={"dates": dates, "prices": prices})
    except Exception as e:
        return JSONResponse(content={"dates": [], "prices": [], "error": str(e)})
