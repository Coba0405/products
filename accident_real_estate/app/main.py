from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.db.database import Base, engine
from app.models import Property, PropertyImage  # noqa: F401 テーブル生成のためインポート
from app.routers.properties import router as properties_router, IMAGES_DIR

app = FastAPI(title="事故物件管理アプリ")

# 起動時にテーブルを自動生成
Base.metadata.create_all(bind=engine)

# 画像ディレクトリを確実に作成
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
Path("data").mkdir(parents=True, exist_ok=True)

# 静的ファイル
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 画像ファイルを公開
app.mount("/images", StaticFiles(directory=str(IMAGES_DIR)), name="images")

# ルーター登録
app.include_router(properties_router)
