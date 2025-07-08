import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
apod_api_key = os.getenv("APOD_API_KEY")
url = f"https://api.nasa.gov/planetary/apod?api_key={apod_api_key}"

# deepl_api_key = os.getenv("DEEPL_API_KEY")

response = requests.get(url)
data = response.json()

filename = 'apod.json'

# ファイルが存在していれば読み込む、なければ空のリストを作る
if os.path.isfile(filename):
    with open('apod.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
else:
    data_list = []
data_list.append(data)

with open(filename, 'w', encoding='utf-8') as file:
    json.dump(data_list, file, indent=4, ensure_ascii=False)

print(data)
# print(data["title"])
# print(data["explanation"])
# print(data["url"])
