import os
import requests
import json
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

url = "https://api.nasa.gov/planetary/earth/imagery"
# 画像を取得したい地点と日付
params = {
    "lon": 139.6917,
    "lat": 35.6895,
    "date": "2020-06-01",
    "dim": 0.1,
    "api_key": API_KEY
}

# APIリクエストの実行
try:
    response =requests.get(url, params=params)
    response.raise_for_status() #エラーがあればexceptへ投げる

    with open("tokyo_satellite.jpg", "wb") as file:
        file.write(response.content)
    print("画像の保存に成功しました")
   
except requests.exceptions.HTTPError as http_err:
    print("HTTPエラー:", http_err)
    print("レスポンス内容:", response.text)
except Exception as e:
    print("その他のエラー:", e)
    print(f"その他のエラー: {e}")

# img = Image.open("tokyo_satellite.jpg")
# img.show()
