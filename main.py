import httpx
import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory="static"), name="static")

DATABASE_URL = "postgresql://kabukan_db_user:Az24e9htLyLe0ragXvuAWLgfyRzvyXIM@dpg-d95pli6q1p3s73dbm6a0-a/kabukan_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Stock(Base):
    __tablename__ = "stocks"
    id = Column(String, primary_key=True)
    code = Column(String, unique=True, index=True)
    name = Column(String)
    price = Column(Float)

class Dividend(Base):
    __tablename__ = "dividends"
    id = Column(String, primary_key=True)
    code = Column(String, unique=True, index=True)
    name = Column(String)
    annual_dividend = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

STOCKS = [
{"code":"7203","name":"トヨタ自動車"},{"code":"6758","name":"ソニーグループ"},{"code":"9984","name":"ソフトバンクグループ"},{"code":"7974","name":"任天堂"},{"code":"6861","name":"キーエンス"},{"code":"8035","name":"東京エレクトロン"},{"code":"6098","name":"リクルートホールディングス"},{"code":"4063","name":"信越化学工業"},{"code":"7267","name":"本田技研工業"},{"code":"8306","name":"三菱UFJフィナンシャル・グループ"},{"code":"8316","name":"三井住友フィナンシャルグループ"},{"code":"8411","name":"みずほフィナンシャルグループ"},{"code":"9432","name":"日本電信電話"},{"code":"9433","name":"KDDI"},{"code":"9434","name":"ソフトバンク"},{"code":"4519","name":"中外製薬"},{"code":"4568","name":"第一三共"},{"code":"2914","name":"日本たばこ産業"},{"code":"7751","name":"キヤノン"},{"code":"6954","name":"ファナック"},{"code":"6367","name":"ダイキン工業"},{"code":"4661","name":"オリエンタルランド"},{"code":"7741","name":"HOYA"},{"code":"6762","name":"TDK"},{"code":"3382","name":"セブン＆アイ・ホールディングス"},{"code":"8001","name":"伊藤忠商事"},{"code":"8031","name":"三井物産"},{"code":"8058","name":"三菱商事"},{"code":"8053","name":"住友商事"},{"code":"7201","name":"日産自動車"},{"code":"7202","name":"いすゞ自動車"},{"code":"6902","name":"デンソー"},{"code":"6981","name":"村田製作所"},{"code":"6503","name":"三菱電機"},{"code":"6501","name":"日立製作所"},{"code":"6702","name":"富士通"},{"code":"6701","name":"日本電気"},{"code":"4307","name":"野村総合研究所"},{"code":"8725","name":"MS＆ADインシュアランスグループ"},{"code":"8750","name":"第一生命ホールディングス"},{"code":"8766","name":"東京海上ホールディングス"},{"code":"5803","name":"フジクラ"},{"code":"285A","name":"キオクシアホールディングス"},{"code":"7011","name":"三菱重工業"},{"code":"7013","name":"IHI"},{"code":"7012","name":"川崎重工業"},{"code":"6326","name":"クボタ"},{"code":"5401","name":"日本製鉄"},{"code":"5411","name":"JFEホールディングス"},{"code":"4452","name":"花王"},{"code":"4911","name":"資生堂"},{"code":"2502","name":"アサヒグループホールディングス"},{"code":"2503","name":"キリンホールディングス"},{"code":"2801","name":"キッコーマン"},{"code":"9020","name":"東日本旅客鉄道"},{"code":"9022","name":"東海旅客鉄道"},{"code":"9021","name":"西日本旅客鉄道"},{"code":"9101","name":"日本郵船"},{"code":"9104","name":"商船三井"},{"code":"9107","name":"川崎汽船"},{"code":"8802","name":"三菱地所"},{"code":"8801","name":"三井不動産"},{"code":"9501","name":"東京電力ホールディングス"},{"code":"9502","name":"中部電力"},{"code":"9503","name":"関西電力"},{"code":"5016","name":"JX金属"},{"code":"4523","name":"エーザイ"},{"code":"4578","name":"大塚ホールディングス"},{"code":"4151","name":"協和キリン"},{"code":"6645","name":"オムロン"},{"code":"6723","name":"ルネサスエレクトロニクス"},{"code":"8591","name":"オリックス"},{"code":"7309","name":"シマノ"},{"code":"9602","name":"東宝"},{"code":"4755","name":"楽天グループ"},{"code":"3659","name":"ネクソン"},{"code":"4689","name":"LINEヤフー"},{"code":"2413","name":"エムスリー"},{"code":"6301","name":"小松製作所"},{"code":"7832","name":"バンダイナムコホールディングス"},{"code":"9766","name":"コナミグループ"},{"code":"2269","name":"明治ホールディングス"},{"code":"2282","name":"日本ハム"},{"code":"8267","name":"イオン"},{"code":"3099","name":"三越伊勢丹ホールディングス"},{"code":"8233","name":"高島屋"}
]

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/search")
async def search(q: str = Query(...)):
    results = [s for s in STOCKS if q in s["name"] or q.lower() in s["name"].lower()]
    if not results:
        try:
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.get("https://query1.finance.yahoo.com/v1/finance/search",
                    params={"q": q, "lang": "en-US", "region": "JP", "quotesCount": 10},
                    headers={"User-Agent": "Mozilla/5.0"})
                data = r.json()
                for item in data.get("quotes", []):
                    symbol = item.get("symbol", "")
                    if symbol.endswith(".T"):
                        code = symbol.replace(".T", "")
                        name = item.get("longname") or item.get("shortname") or code
                        results.append({"code": code, "name": name})
        except:
            pass
    return JSONResponse(content={"results": results[:10]}, media_type="application/json; charset=utf-8")

@app.get("/quotes")
async def quotes(codes: str = Query(...)):
    cl = [c.strip() for c in codes.split(",") if c.strip()]
    out = []
    for code in cl:
        try:
            async with httpx.AsyncClient(timeout=15, follow_redirects=True) as c:
                r = await c.get(f"https://query2.finance.yahoo.com/v8/finance/chart/{code}.T",
                    params={"interval": "1d", "range": "2mo"},
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36", "Accept": "application/json"})
                data = r.json()
                result = data["chart"]["result"][0]
                meta = result["meta"]
                price = meta.get("regularMarketPrice")
                prev = meta.get("chartPreviousClose")
                name = next((s["name"] for s in STOCKS if s["code"]==code), None) or meta.get("longName") or meta.get("shortName") or code
                vol = meta.get("regularMarketVolume")
                closes = result["indicators"]["quote"][0]["close"]
                closes = [p for p in closes if p is not None]
                ma25 = sum(closes[-25:]) / min(25, len(closes)) if len(closes) >= 5 else None
                deviation = round((price - ma25) / ma25 * 100, 2) if ma25 and price else None
                avg_vol = sum([v for v in result["indicators"]["quote"][0].get("volume",[]) if v]) / max(1, len([v for v in result["indicators"]["quote"][0].get("volume",[]) if v]))
                if deviation is not None:
                    if deviation < -5 and vol and vol > avg_vol:
                        judgment = "買い候補"
                    elif deviation > 10:
                        judgment = "警戒"
                    else:
                        judgment = "中立"
                else:
                    judgment = "中立"
                change = round(price - prev, 1) if price and prev else None
                pct = round((price - prev) / prev * 100, 2) if price and prev else None
                out.append({"code": code, "name": name, "price": price, "prevClose": prev, "change": change, "changePct": pct, "volume": vol, "deviation": deviation, "judgment": judgment})
        except Exception as e:
            out.append({"code": code, "error": str(e)})
    return JSONResponse(content={"quotes": out}, media_type="application/json; charset=utf-8")

@app.get("/history/{code}")
async def history(code: str):
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as c:
            r = await c.get(f"https://query2.finance.yahoo.com/v8/finance/chart/{code}.T",
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

@app.post("/add-stock")
async def add_stock(code: str = Query(...), name: str = Query(...)):
    db = SessionLocal()
    try:
        stock = Stock(id=f"{code}_{datetime.now().timestamp()}", code=code, name=name, price=0)
        db.add(stock)
        db.commit()
        return {"status": "ok", "code": code}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()

@app.get("/get-stocks")
async def get_stocks():
    db = SessionLocal()
    try:
        stocks = db.query(Stock).all()
        return {"stocks": [{"code": s.code, "name": s.name} for s in stocks]}
    finally:
        db.close()

@app.delete("/delete-stock")
async def delete_stock(code: str = Query(...)):
    db = SessionLocal()
    try:
        db.query(Stock).filter(Stock.code == code).delete()
        db.commit()
        return {"status": "ok"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()

@app.post("/add-dividend")
async def add_dividend(code: str = Query(...), name: str = Query(...), annual_dividend: float = Query(...)):
    db = SessionLocal()
    try:
        dividend = Dividend(id=f"{code}_{datetime.now().timestamp()}", code=code, name=name, annual_dividend=annual_dividend)
        db.add(dividend)
        db.commit()
        return {"status": "ok", "code": code}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()

@app.get("/get-dividends")
async def get_dividends():
    db = SessionLocal()
    try:
        dividends = db.query(Dividend).all()
        return {"dividends": [{"code": d.code, "name": d.name, "annual_dividend": d.annual_dividend} for d in dividends]}
    finally:
        db.close()

@app.delete("/delete-dividend")
async def delete_dividend(code: str = Query(...)):
    db = SessionLocal()
    try:
        db.query(Dividend).filter(Dividend.code == code).delete()
        db.commit()
        return {"status": "ok"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()

@app.get("/dividend-yield/{code}")
async def dividend_yield(code: str):
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as c:
            r = await c.get(f"https://query2.finance.yahoo.com/v8/finance/chart/{code}.T",
                params={"interval": "1d", "range": "2mo"},
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36", "Accept": "application/json"})
            data = r.json()
            result = data["chart"]["result"][0]
            ts = result["timestamp"]
            closes = result["indicators"]["quote"][0]["close"]
            
        db = SessionLocal()
        dividend = db.query(Dividend).filter(Dividend.code == code).first()
        db.close()
        
        if not dividend:
            return JSONResponse(content={"error": "Dividend not found"})
        
        from datetime import datetime
        dates = [datetime.fromtimestamp(t).strftime("%Y-%m-%d") for t in ts]
        yields = []
        for price in closes:
            if price:
                yield_pct = round((dividend.annual_dividend / price) * 100, 2)
                yields.append(yield_pct)
            else:
                yields.append(None)
        
        return JSONResponse(content={"dates": dates, "yields": yields, "current_yield": yields[-1] if yields[-1] else 0})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})

@app.get("/dividend-yield-at-purchase/{code}")
async def dividend_yield_at_purchase(code: str):
    db = SessionLocal()
    try:
        dividend = db.query(Dividend).filter(Dividend.code == code).first()
        if not dividend:
            return JSONResponse(content={"error": "Dividend not found"})
        db.close()
        
        # 保有株から取得単価を取得する（Holdテーブルにアクセス）
        # ここでは、localStorageから取得した保有株データを使用するため、フロントエンドで計算する
        # バックエンドでは年間配当金を返すのみ
        return JSONResponse(content={"annual_dividend": dividend.annual_dividend})
    except Exception as e:
        db.close()
        return JSONResponse(content={"error": str(e)})
