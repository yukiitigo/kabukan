import requests
import getpass

api_key = getpass.getpass("J-QuantsのAPIキー: ")

headers = {"x-api-key": api_key}

# テスト銘柄: トヨタ自動車 (7203)
code = "7203"
r = requests.get(
    f"https://api.jquants.com/v2/fins/summary?code={code}",
    headers=headers
)
print("財務情報ステータス:", r.status_code)
data = r.json()

if r.status_code == 200 and "data" in data and len(data["data"]) > 0:
    latest = data["data"][0]
    print("\n=== 利用可能な全カラム ===")
    print(list(latest.keys()))
    print("\n=== 最新の財務データ（サンプル） ===")
    print("開示種別 (DocType):", latest.get("DocType"))
    print("開示日 (DiscDate):", latest.get("DiscDate"))
    print("実績EPS (EPS):", latest.get("EPS"))
    print("BPS:", latest.get("BPS"))
    print("会社予想EPS (FEPS):", latest.get("FEPS"))
    print("\n全体のレコード数:", len(data["data"]))
else:
    print("データが取得できませんでした:", data)
