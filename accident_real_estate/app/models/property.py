from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
import enum

from app.db.database import Base


class AccidentType(str, enum.Enum):
    """事故種別"""
    suicide = "自殺"
    homicide = "他殺"
    lonely_death = "孤独死"
    fire = "火災"
    other = "その他"


class ConfirmStatus(str, enum.Enum):
    """確認ステータス"""
    confirmed = "確認済み"
    unconfirmed = "未確認"
    rumor = "噂レベル"


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(500), nullable=False)           # 住所
    accident_type = Column(String(50), nullable=False)      # 事故種別
    confirm_status = Column(String(50), nullable=False,
                            default=ConfirmStatus.unconfirmed)  # 確認ステータス
    summary = Column(Text, nullable=True)                   # 事故概要
    memo = Column(Text, nullable=True)                      # メモ
    map_url = Column(String(1000), nullable=True)           # GoogleマップURL
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 画像（1対多）
    images = relationship("PropertyImage", back_populates="property",
                          cascade="all, delete-orphan")


class PropertyImage(Base):
    __tablename__ = "property_images"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False, index=True)
    filename = Column(String(500), nullable=False)          # 保存ファイル名
    original_filename = Column(String(500), nullable=False) # 元ファイル名
    created_at = Column(DateTime, default=datetime.utcnow)

    property = relationship("Property", back_populates="images")
