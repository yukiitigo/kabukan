import httpx
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory="static"), name="static")

HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/search")
async def search(q: str = Query(...)):
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get("https://query1.finance.yahoo.com/v1/finance/search",
                params={"q": q, "lang": "ja-JP", "region": "JP", "quotesCount": 10},
                headers={"User-Agent": "Mozilla/5.0"})
            data = r.json()
            results = []
            for item in data.get("quotes", []):
                symbol = item.get("symbol", "")
                if symbol.endswith(".T"):
                    code = symbol.replace(".T", "")
                    name = item.get("longname") or item.get("shortname") or code
                    results.append({"code": code, "name": name})
            return JSONResponse(content={"results": results[:10]}, media_type="application/json; charset=utf-8")
    except Exception as e:
        return JSONResponse(content={"results": [], "error": str(e)})

@app.get("/quotes")
async def quotes(codes: str = Query(...)):
    cl = [c.strip() for c in codes.split(",") if c.strip()]
    out = []
    for code in cl:
        try:
            async with httpx.AsyncClient(timeout=15) as c:
                r = await c.get(f"https://finance.yahoo.co.jp/quote/{code}.T",
                    headers=HEADERS)
                text = r.text
                import re
                price_match = re.search(r'"currentPrice"[^}]*?"value":\s*([\d.]+)', text)
                prev_match = re.search(r'"previousClose"[^}]*?"value":\s*([\d.]+)', text)
                name_match = re.search(r'"name":\s*"([^"]+)"', text)
                vol_match = re.search(r'"volume"[^}]*?"value":\s*([\d.]+)', text)
                if price_match:
                    price = float(price_match.group(1))
                    prev = float(prev_match.group(1)) if prev_match else None
                    name = name_match.group(1) if name_match else code
                    vol = int(float(vol_match.group(1))) if vol_match else None
                    change = round(price - prev, 1) if prev else None
                    pct = round((price - prev) / prev * 100, 2) if prev else None
                    out.append({"code": code, "name": name, "price": price, "prevClose": prev, "change": change, "changePct": pct, "volume": vol})
                else:
                    out.append({"code": code, "error": "データ取得失敗"})
        except Exception as e:
            out.append({"code": code, "error": str(e)})
    return JSONResponse(content={"quotes": out}, media_type="application/json; charset=utf-8")

@app.get("/history/{code}")
async def history(code: str):
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{code}.T",
                params={"interval": "1d", "range": "1mo"},
                headers={"User-Agent": "Mozilla/5.0"})
            data = r.json()
            ts = data["chart"]["result"][0]["timestamp"]
            closes = data["chart"]["result"][0]["indicators"]["quote"][0]["close"]
            from datetime import datetime
            dates = [datetime.fromtimestamp(t).strftime("%Y-%m-%d") for t in ts]
            prices = [round(float(p), 1) if p else None for p in closes]
            return JSONResponse(content={"dates": dates, "prices": prices})
    except Exception as e:
        return JSONResponse(content={"dates": [], "prices": [], "error": str(e)})
