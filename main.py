import yfinance as yf
import httpx
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

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
        t = yf.Ticker(code + ".T")
        try:
            info = t.fast_info
            price = info.last_price
            prev = info.previous_close
            change = round(price - prev, 1) if price and prev else None
            pct = round((price - prev) / prev * 100, 2) if price and prev else None
            hist = t.history(period="1d")
            vol = int(hist["Volume"].iloc[-1]) if not hist.empty else None
            name = t.info.get("longName") or t.info.get("shortName") or code
            out.append({"code": code, "name": name, "price": price, "prevClose": prev, "change": change, "changePct": pct, "volume": vol})
        except Exception as e:
            out.append({"code": code, "error": str(e)})
    return JSONResponse(content={"quotes": out}, media_type="application/json; charset=utf-8")

@app.get("/history/{code}")
async def history(code: str):
    try:
        t = yf.Ticker(code + ".T")
        hist = t.history(period="1mo")
        dates = [str(d.date()) for d in hist.index]
        prices = [round(float(p), 1) for p in hist["Close"].tolist()]
        return JSONResponse(content={"dates": dates, "prices": prices})
    except Exception as e:
        return JSONResponse(content={"dates": [], "prices": [], "error": str(e)})
