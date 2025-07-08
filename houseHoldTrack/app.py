import requests
import json

url = "http://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

params = {
    "appId":'58d95338ccddec8cef46ef85c851e3cf4159dffa',
    "statsDataId": "0003000797",
    "lang": "J",
    "metaGetFlg": "Y",
    "cntGetFlg": "N",
    "sectionHeaderFlg": "1",
    "cdArea": "00000",
}

response = requests.get(url, params=params)

if response.status_code == 200:
    try:
        data = response.json()
        values = data["GET_STATS_DATA"]["STATISTICAL_DATA"]["DATA_INF"]["VALUE"]

        # print(data)

        cat01_dict = {}
        for item in data["GET_STATS_DATA"]["STATISTICAL_DATA"]["CLASS_INF"]["CLASS_OBJ"]:
            if item["@id"] == "cat01":
                    for val in item["CLASS"]:
                         cat01_dict[val["@code"]] = val["@name"]

        result_list = []
        # 年度と金額だけを抽出
        for value in values:
            year = value["@time"][:4]
            money = value["$"]
            cat01 = value["@cat01"]
            name = cat01_dict.get(cat01, "不明な項目")

            result_list.append({
                "年": year,
                "項目": name,
                "金額": money
            })

        with open("household_income.json", "w", encoding='utf-8') as file:
            json.dump(result_list, file, indent=4, ensure_ascii=False)

        print("データをhousehold_income.jsonに保存しました")

    except json.JSONDecodeError as e:
        print("JSONデコードエラー:", e)
else:
    print("リクエスト失敗", response.status_code)
