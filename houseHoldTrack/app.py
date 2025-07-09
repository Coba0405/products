import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

appId_estat = '58d95338ccddec8cef46ef85c851e3cf4159dffa'
url = "http://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

params = {
    "appId": appId_estat,
    "lang": "J",
    "statsDataId": "0003000799",
    "metaGetFlg": "Y",
    "cntGetFlg": "N",
    "explanationGetFlg": "Y",
    "annotationGetFlg": "Y",
    "sectionHeaderFlg": "1",
    "replaceSpChars": "0",
    "cdArea": "00000",
    "cdCat01": "019,058,205"
}

response = requests.get(url, params=params)
jsonData = response.json()

print(len(jsonData), jsonData.keys())
print(len(jsonData['GET_STATS_DATA']), jsonData['GET_STATS_DATA'].keys())
data_static = jsonData['GET_STATS_DATA']['STATISTICAL_DATA']
print(len(data_static), data_static.keys())

if response.status_code == 200:
    try:
        data = response.json()
        values = data_static["DATA_INF"]["VALUE"]

        cat01_dict = {}
        for class_obj in data["GET_STATS_DATA"]["STATISTICAL_DATA"]["CLASS_INF"]["CLASS_OBJ"]:
            if class_obj["@id"] == "cat01":
                for item in class_obj["CLASS"]:
                    cat01_dict[item["@code"]] =  item["@name"]

        data_list = []
        for item in values:
            year = item["@time"][:4]
            item_code = item["@cat01"]
            amount = float(item["$"])
            item_name = cat01_dict.get(item_code, "不明な項目")
            data_list.append([year, item_name, amount])

        df = pd.DataFrame(data_list, columns=["年", "項目", "金額"])
        df_grouped = df.groupby(['年', '項目'])['金額'].mean().reset_index()
        # df["金額"] = df["金額"].astype(int)
        # print(df.head(50))

        for item_name in df_grouped["項目"].unique():
            subset = df_grouped[df_grouped["項目"] == item_name]
            plt.plot(subset["年"], subset["金額"], marker='o', label=item_name)

        # for item in df["項目"].unique():
        #     subset = df[df["項目"] == item_name]
        #     plt.plot(subset["年"], subset["金額"], label=item_name)

        plt.xlabel("年")
        plt.ylabel("金額")
        plt.title("収入・支出・預貯金の推移")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print("処理中にエラー:", e)
else:
    print("リクエスト失敗", response.status_code)
