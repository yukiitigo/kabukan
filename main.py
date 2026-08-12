import httpx
import os
import requests
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory="static"), name="static")




JQUANTS_API_KEY = os.environ.get("JQUANTS_API_KEY", "")

def get_jquants_financial_data(code):
    try:
        headers = {"x-api-key": JQUANTS_API_KEY}
        r = requests.get(f"https://api.jquants.com/v2/fins/summary?code={code}", headers=headers, timeout=15)
        if r.status_code != 200:
            return None
        data = r.json()
        return data.get("data", [])
    except Exception:
        return None

def get_jquants_price_on_date(code, date_str):
    try:
        headers = {"x-api-key": JQUANTS_API_KEY}
        r = requests.get(f"https://api.jquants.com/v2/equities/bars/daily?code={code}&date={date_str}", headers=headers, timeout=15)
        if r.status_code != 200:
            return None
        data = r.json()
        items = data.get("data", [])
        if items:
            return items[0].get("AdjC")
        return None
    except Exception:
        return None

TRADING_CO = {"8001","8002","8015","8031","8053","8058","2768"}

STOCKS = [
{"code":"7203","name":"トヨタ自動車"},{"code":"6758","name":"ソニーグループ"},{"code":"9984","name":"ソフトバンクグループ"},{"code":"7974","name":"任天堂"},{"code":"6861","name":"キーエンス"},{"code":"8035","name":"東京エレクトロン"},{"code":"6098","name":"リクルートホールディングス"},{"code":"4063","name":"信越化学工業"},{"code":"7267","name":"本田技研工業"},{"code":"8306","name":"三菱UFJフィナンシャル・グループ"},{"code":"8316","name":"三井住友フィナンシャルグループ"},{"code":"8411","name":"みずほフィナンシャルグループ"},{"code":"9432","name":"日本電信電話"},{"code":"9433","name":"KDDI"},{"code":"9434","name":"ソフトバンク"},{"code":"4519","name":"中外製薬"},{"code":"4568","name":"第一三共"},{"code":"2914","name":"日本たばこ産業"},{"code":"7751","name":"キヤノン"},{"code":"6954","name":"ファナック"},{"code":"6367","name":"ダイキン工業"},{"code":"4661","name":"オリエンタルランド"},{"code":"7741","name":"HOYA"},{"code":"6762","name":"TDK"},{"code":"3382","name":"セブン＆アイ・ホールディングス"},{"code":"8001","name":"伊藤忠商事"},{"code":"8031","name":"三井物産"},{"code":"8058","name":"三菱商事"},{"code":"8053","name":"住友商事"},{"code":"7201","name":"日産自動車"},{"code":"7202","name":"いすゞ自動車"},{"code":"6902","name":"デンソー"},{"code":"6981","name":"村田製作所"},{"code":"6503","name":"三菱電機"},{"code":"6501","name":"日立製作所"},{"code":"6702","name":"富士通"},{"code":"6701","name":"日本電気"},{"code":"4307","name":"野村総合研究所"},{"code":"8725","name":"MS＆ADインシュアランスグループ"},{"code":"8750","name":"第一生命ホールディングス"},{"code":"8766","name":"東京海上ホールディングス"},{"code":"5803","name":"フジクラ"},{"code":"285A","name":"キオクシアホールディングス"},{"code":"7011","name":"三菱重工業"},{"code":"7013","name":"IHI"},{"code":"7012","name":"川崎重工業"},{"code":"6326","name":"クボタ"},{"code":"5401","name":"日本製鉄"},{"code":"5445","name":"東京鐵鋼"},{"code":"4452","name":"花王"},{"code":"4911","name":"資生堂"},{"code":"2502","name":"アサヒグループホールディングス"},{"code":"2503","name":"キリンホールディングス"},{"code":"2801","name":"キッコーマン"},{"code":"9020","name":"東日本旅客鉄道"},{"code":"9022","name":"東海旅客鉄道"},{"code":"9021","name":"西日本旅客鉄道"},{"code":"9101","name":"日本郵船"},{"code":"9104","name":"商船三井"},{"code":"9107","name":"川崎汽船"},{"code":"8802","name":"三菱地所"},{"code":"8801","name":"三井不動産"},{"code":"9501","name":"東京電力ホールディングス"},{"code":"9502","name":"中部電力"},{"code":"9503","name":"関西電力"},{"code":"5016","name":"JX金属"},{"code":"4523","name":"エーザイ"},{"code":"4578","name":"大塚ホールディングス"},{"code":"4151","name":"協和キリン"},{"code":"6645","name":"オムロン"},{"code":"6723","name":"ルネサスエレクトロニクス"},{"code":"8591","name":"オリックス"},{"code":"7309","name":"シマノ"},{"code":"9602","name":"東宝"},{"code":"4755","name":"楽天グループ"},{"code":"3659","name":"ネクソン"},{"code":"4689","name":"LINEヤフー"},{"code":"2413","name":"エムスリー"},{"code":"6301","name":"小松製作所"},{"code":"7832","name":"バンダイナムコホールディングス"},{"code":"9766","name":"コナミグループ"},{"code":"2269","name":"明治ホールディングス"},{"code":"2282","name":"日本ハム"},{"code":"8267","name":"イオン"},{"code":"3099","name":"三越伊勢丹ホールディングス"},{"code":"8233","name":"高島屋"},{"code":"6920","name":"レーザーテック"},{"code":"6857","name":"アドバンテスト"},{"code":"6146","name":"ディスコ"},{"code":"4023","name":"クレスコ"},{"code":"3653","name":"ボーダー"},{"code":"3906","name":"HANATOUR"},{"code":"3932","name":"アロン"},{"code":"4768","name":"大塚ホールディングス"},{"code":"6702","name":"富士通"},{"code":"9684","name":"スクウェア・エニックス"},{"code":"6981","name":"村田製作所"},{"code":"6728","name":"アルバック"},{"code":"9470","name":"東京オリンピック"},{"code":"6741","name":"日本テレコム"},{"code":"9433","name":"KDDI"},{"code":"3753","name":"フレアス"},{"code":"6753","name":"シャープ"},{"code":"4967","name":"小松製作所"},{"code":"7731","name":"ニコン"},{"code":"6273","name":"SMC"},{"code":"6954","name":"ファナック"},{"code":"7226","name":"極東開発工業"},{"code":"6463","name":"TPR"},{"code":"1414","name":"ショーボンドホールディングス"},{"code":"6718","name":"アイホン"}
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
                name = next((s["name"] for s in STOCKS if s["code"]==code), None) or code
                vol = meta.get("regularMarketVolume")
                closes = result["indicators"]["quote"][0]["close"]
                closes = [p for p in closes if p is not None]
                ma25 = sum(closes[-25:]) / min(25, len(closes)) if len(closes) >= 20 else None
                deviation = round((price - ma25) / ma25 * 100, 2) if ma25 and price else None
                _vhist = [v for v in result["indicators"]["quote"][0].get("volume", []) if v]
                _vhist = _vhist[:-1][-25:] if len(_vhist) > 1 else []
                avg_vol = (sum(_vhist) / len(_vhist)) if _vhist else None
                if ma25 is None:
                    judgment = "判定不能"
                elif deviation is not None:
                    if deviation < -5 and vol and avg_vol and vol > avg_vol:
                        judgment = "買い候補"
                    elif deviation > 10:
                        judgment = "警戒"
                    else:
                        judgment = "中立"
                else:
                    judgment = "判定不能"
                change = round(price - prev, 1) if price and prev else None
                pct = round((price - prev) / prev * 100, 2) if price and prev else None
                out.append({"code": code, "name": name, "price": price, "prevClose": prev, "change": change, "changePct": pct, "volume": vol, "deviation": deviation, "judgment": judgment, "ma25": round(ma25, 1) if ma25 else None, "avgVolume": round(avg_vol) if avg_vol else None})
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
            volumes = result["indicators"]["quote"][0].get("volume", [])
            return JSONResponse(content={"dates": dates, "prices": prices, "volumes": volumes})
    except Exception as e:
        return JSONResponse(content={"dates": [], "prices": [], "error": str(e)})

@app.get("/fair-value/{code}")
async def fair_value(code: str):
    try:
        statements = get_jquants_financial_data(code)
        if not statements:
            return JSONResponse(content={"error": "no financial data"})
        fy_records = [s for s in statements if "FY" in s.get("DocType", "") and s.get("NP") and s.get("Eq")]
        fy_records.sort(key=lambda x: x.get("DiscDate", ""), reverse=True)
        if len(fy_records) < 1:
            return JSONResponse(content={"error": "insufficient data"})
        latest = fy_records[0]
        roe = None
        if latest.get("NP") and latest.get("Eq") and float(latest["Eq"]) != 0:
            roe = float(latest["NP"]) / float(latest["Eq"]) * 100
        equity_ratio = float(latest["EqAR"]) * 100 if latest.get("EqAR") else None
        op_margin = None
        if latest.get("OP") and latest.get("Sales") and float(latest["Sales"]) != 0:
            op_margin = float(latest["OP"]) / float(latest["Sales"]) * 100
        profit_trend = None
        if len(fy_records) >= 2:
            prev_np = fy_records[1].get("NP")
            if prev_np and latest.get("NP"):
                profit_trend = "増益" if float(latest["NP"]) > float(prev_np) else "減益"
        net_margin = None
        if latest.get("NP") and latest.get("Sales") and float(latest["Sales"]) != 0:
            net_margin = float(latest["NP"]) / float(latest["Sales"]) * 100
        profile = "商社" if str(code) in TRADING_CO else "標準"
        roe_lo, eqr_min = (10, 30) if profile == "商社" else (15, 40)
        roe_hi = 30
        margin_val, margin_min, margin_label = (net_margin, 3, "純利益率") if profile == "商社" else (op_margin, 10, "営業利益率")
        score = 0
        reasons = []
        if roe is not None:
            if roe_lo <= roe <= roe_hi:
                score += 1
                reasons.append(f"ROE{roe_lo}-{roe_hi}%（優良水準）")
            elif roe > roe_hi:
                reasons.append("ROE30%超（レバレッジ過多の可能性、要確認）")
            elif roe < 5:
                reasons.append("ROE5%未満")
        if equity_ratio is not None:
            if equity_ratio >= eqr_min:
                score += 1
                reasons.append(f"自己資本比率{eqr_min}%以上")
            elif equity_ratio < 20:
                reasons.append("自己資本比率20%未満（財務レバレッジ高）")
        if profit_trend == "増益":
            score += 1
            reasons.append("増益トレンド")
        elif profit_trend == "減益":
            reasons.append("減益トレンド")
        if margin_val is not None and margin_val >= margin_min:
            score += 1
            reasons.append(f"{margin_label}{margin_min}%以上")
        if profile == "商社":
            reasons.append("商社プロファイルで判定（低マージン・高レバレッジ構造を考慮）")
        available = sum(1 for x in [roe, equity_ratio, margin_val, profit_trend] if x is not None)
        if available < 3:
            rating = "判定不能"
        elif score >= 3:
            rating = "優良"
        elif score >= 2:
            rating = "普通"
        else:
            rating = "要注意"

        per_list = []
        pbr_list = []
        latest_bps = None
        latest_eps = None
        for s in fy_records:
            disc_date = s.get("DiscDate")
            eps = s.get("EPS")
            bps = s.get("BPS")
            if bps:
                price = get_jquants_price_on_date(code, disc_date.replace("-", ""))
                if price and eps and float(eps) > 0:
                    per_list.append(price / float(eps))
                if price and bps and float(bps) > 0:
                    pbr_list.append(price / float(bps))
                if latest_bps is None:
                    latest_bps = float(bps)
            if eps and latest_eps is None:
                latest_eps = float(eps)
        valuation = None
        fair_price = None
        avg_per = None
        avg_pbr = None
        if per_list and pbr_list and latest_bps and latest_eps:
            avg_per = sum(per_list) / len(per_list)
            avg_pbr = sum(pbr_list) / len(pbr_list)
            fair_price = (latest_eps * avg_per + latest_bps * avg_pbr) / 2

        return JSONResponse(content={
            "rating": rating, "score": score, "available": available, "profile": profile,
            "roe_lo": roe_lo, "roe_hi": roe_hi, "eqr_min": eqr_min,
            "margin_label": margin_label, "margin_min": margin_min,
            "margin_val": round(margin_val, 1) if margin_val is not None else None,
            "roe": round(roe, 1) if roe is not None else None,
            "equity_ratio": round(equity_ratio, 1) if equity_ratio is not None else None,
            "op_margin": round(op_margin, 1) if op_margin is not None else None,
            "profit_trend": profit_trend, "reasons": reasons,
            "fair_price": round(fair_price, 1) if fair_price else None,
            "avg_per": round(avg_per, 2) if avg_per else None,
            "avg_pbr": round(avg_pbr, 2) if avg_pbr else None,
            "sample_size": len(per_list)
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)})


@app.get("/dividend-yield/{code}")
async def dividend_yield(code: str, dividend: float = 0):
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as c:
            r = await c.get(f"https://query2.finance.yahoo.com/v8/finance/chart/{code}.T",
                params={"interval": "1d", "range": "2mo"},
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36", "Accept": "application/json"})
            data = r.json()
            result = data["chart"]["result"][0]
            ts = result["timestamp"]
            closes = result["indicators"]["quote"][0]["close"]
            
        if not dividend or dividend <= 0:
            return JSONResponse(content={"error": "dividend param required"})
        
        from datetime import datetime
        dates = [datetime.fromtimestamp(t).strftime("%Y-%m-%d") for t in ts]
        yields = []
        for price in closes:
            if price:
                yield_pct = round((dividend / price) * 100, 2)
                yields.append(yield_pct)
            else:
                yields.append(None)
        
        return JSONResponse(content={"dates": dates, "yields": yields, "current_yield": (yields[-1] or 0) if yields else 0})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})


@app.get("/verify-stocks")
async def verify_stocks():
    import collections
    headers = {"x-api-key": JQUANTS_API_KEY}
    used, items = None, []
    for url in ["https://api.jquants.com/v2/equities/info",
                "https://api.jquants.com/v2/listed/info",
                "https://api.jquants.com/v1/listed/info"]:
        try:
            r = requests.get(url, headers=headers, timeout=30)
            if r.status_code == 200:
                j = r.json()
                items = j.get("data") or j.get("info") or []
                if items:
                    used = url
                    break
        except Exception:
            pass
    if not items:
        return JSONResponse(content={"error": "listed info not available"})
    master = {}
    for it in items:
        c = str(it.get("Code") or it.get("code") or "")
        n = it.get("CompanyName") or it.get("Name") or it.get("name") or ""
        if c:
            master[c] = n
            if len(c) == 5 and c.endswith("0"):
                master[c[:4]] = n
    dup = [c for c, k in collections.Counter(s["code"] for s in STOCKS).items() if k > 1]
    notfound, mismatch = [], []
    for s in STOCKS:
        official = master.get(s["code"])
        if official is None:
            notfound.append(s["code"] + " " + s["name"])
        elif official.replace(" ", "").replace("　", "") != s["name"].replace(" ", "").replace("　", ""):
            mismatch.append({"code": s["code"], "app": s["name"], "official": official})
    return JSONResponse(content={"endpoint": used, "total": len(STOCKS),
                                 "dup_count": len(dup), "duplicates": dup,
                                 "notfound_count": len(notfound), "not_found": notfound,
                                 "mismatch_count": len(mismatch), "name_mismatch": mismatch})
@app.get("/verify-stocks")
async def verify_stocks():
    import collections
    headers = {"x-api-key": JQUANTS_API_KEY}
    r = requests.get("https://api.jquants.com/v2/equities/master", headers=headers, timeout=60)
    if r.status_code != 200:
        return JSONResponse(content={"error": "status %d" % r.status_code, "body": r.text[:300]})
    j = r.json()
    items = j.get("data") or []
    if not items:
        return JSONResponse(content={"error": "empty", "keys": list(j.keys())})
    sample = items[0]
    ckey = next((k for k in sample if k.lower() in ("code", "localcode", "c")), None)
    nkey = next((k for k in sample if "name" in k.lower() and "eng" not in k.lower()), None)
    if not ckey or not nkey:
        return JSONResponse(content={"error": "field not detected", "sample": sample})
    master = {}
    for it in items:
        c = str(it.get(ckey) or "")
        n = it.get(nkey) or ""
        if c:
            master[c] = n
            if len(c) == 5 and c.endswith("0"):
                master[c[:4]] = n
    dup = [c for c, k in collections.Counter(s["code"] for s in STOCKS).items() if k > 1]
    notfound, mismatch = [], []
    for s in STOCKS:
        o = master.get(s["code"])
        if o is None:
            notfound.append(s["code"] + " " + s["name"])
        elif o.replace(" ", "").replace("　", "") != s["name"].replace(" ", "").replace("　", ""):
            mismatch.append({"code": s["code"], "app": s["name"], "official": o})
    return JSONResponse(content={"master_count": len(items), "code_key": ckey, "name_key": nkey,
                                 "sample": sample, "total": len(STOCKS), "duplicates": dup,
                                 "not_found": notfound, "name_mismatch": mismatch})
