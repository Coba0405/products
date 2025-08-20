FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci || npm install

# ソースは開発では volume で上書きされるが、コピーしておいてもOK
COPY . .

EXPOSE 5173
# 実行コマンドは docker-compose 側に記載
