import requests
import json

url = "http://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

params = {
    "appId":'58d95338ccddec8cef46ef85c851e3cf4159dffa',
    "statsDataId": "0004023601",
    "lang": "J",
    "metaGetFlg": "N",
    "cntGetFlg": "N",
    "sectionHeaderFlg": "1",
    "cdArea": "00000",
}

response = requests.get(url, params=params)

if response.status_code == 200:
    try:
        data = response.json()
        # print(json.dumps(data, indent=4, ensure_ascii=False))
        values = data["GET_STATS_DATA"]["STATISTICAL_DATA"]["DATA_INF"]["VALUE"]
        # 粘土と金額だけを抽出
        for entry in values:
            year = entry["@time"]
            amount = entry["$"]
            print(f"{year}年: {amount}円")
    except json.JSONDecodeError as e:
        print("JSONデコードエラー:", e)
else:
    print("リクエスト失敗", response.status_code)
