FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# アプリ本体は volume でマウントするが、初回ビルド時のためにコピーしておいてもOK
COPY . .

EXPOSE 5000
# 実行コマンドは docker-compose 側に記載