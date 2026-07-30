import requests
import getpass

api_key = getpass.getpass("J-QuantsのAPIキー: ")
headers = {"x-api-key": api_key}

# テスト銘柄: トヨタ自動車 (7203)
code = "7203"
r = requests.get(
    f"https://api.jquants.com/v2/equities/bars/daily?code={code}&date=20240508",
    headers=headers
)
print("株価情報ステータス:", r.status_code)
data = r.json()
print(data)
