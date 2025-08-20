FROM node:20-alpine

WORKDIR /app

# 依存関係を先に入れてキャッシュを効かせる
COPY package*.json ./
RUN npm ci || npm install

# 実際のソース。開発では volume で上書きされるので省略可だが、入れてもOK
COPY . .

EXPOSE 5173
# 実行コマンドは compose 側の command を使用