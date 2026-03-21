import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/accident_real_estate.db")

# SQLiteのスレッドチェックを無効化（FastAPIの非同期処理対応）
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """DBセッションのDI用ジェネレータ"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
