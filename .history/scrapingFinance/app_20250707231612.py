import os
import requests
import json
import schedule
import time
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
TO_USER_ID = os.getenv("TO_USER_ID")

# パピレスのデータを送信
def send_message(text):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        "Content-Type": "application/json"
    }

    body = {
        "to": TO_USER_ID,
        "messages": [{
            "type": "text",
            "text": text
        }]
    }

    response = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, data=json.dumps(body))
    print("送信結果:", response.status_code)

# パピレスのデータを取得
def get_stock_info():
    url = "https://finance.yahoo.co.jp/quote/3641.T"
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    # 全ての価格を取得
    price_spans = soup.find_all("span", class_="StyledNumber__value__3rXW")
    name_tag = soup.find("h1")
    today = datetime.today().strftime('%Y年%m月%d日 (%a)')

    try:
        message = f"""
        取得日: {today}
        {name_tag.text} 株価情報
        前日終値: {price_spans[3].text}
        始値: {price_spans[4].text}
        高値: {price_spans[5].text}
        安値: {price_spans[6].text}
        終値: {price_spans[0].text}
        PER : {price_spans[16].text}
        PBR : {price_spans[17].text}
        """
    except IndexError:
        message = f"{name_tag} のデータ取得に失敗しました。"

    print(message)
    return message.strip()

def job():
    stock_info = get_stock_info()
    send_message(stock_info)

schedule.every().monday.at("15:05").do(job)
schedule.every().monday.at("20:44").do(job)
schedule.every().tuesday.at("15:05").do(job)
schedule.every().wednesday.at("15:05").do(job)
schedule.every().thursday.at("15:05").do(job)
schedule.every().friday.at("15:05").do(job)

# ループ実行（終了させない）
print("スケジューラーが起動しました")
while True:
    schedule.run_pending()
    time.sleep(1)

if __name__ == "__main__":
    stock_info = get_stock_info()
    send_message(stock_info)

# print(len(price_spans))

# for i, span in enumerate(price_spans):
#     parent = span.find_parent()
#     print(f"----- {i} -----")
#     print(parent.text)

