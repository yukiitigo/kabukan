import httpx
import json

r = httpx.get("https://query1.finance.yahoo.com/v1/finance/search",
    params={"q": "fujikura", "lang": "ja-JP", "region": "JP", "quotesCount": 10},
    headers={"User-Agent": "Mozilla/5.0"})

print("encoding:", r.encoding)
print("raw:", r.content[:200])
print("json:", r.json())
