import os
import re
import uuid
from pathlib import Path
from typing import Optional
from urllib.parse import parse_qs, urlparse

from fastapi import APIRouter, Depends, Form, HTTPException, Request, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.property import AccidentType, ConfirmStatus, Property, PropertyImage

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

IMAGES_DIR = Path(os.getenv("IMAGES_DIR", "./images"))


def _save_image(file: UploadFile) -> str:
    """画像をIMAGES_DIRに保存し、保存ファイル名を返す"""
    ext = Path(file.filename).suffix.lower()
    filename = f"{uuid.uuid4().hex}{ext}"
    dest = IMAGES_DIR / filename
    with open(dest, "wb") as f:
        f.write(file.file.read())
    return filename


def _delete_image_file(filename: str) -> None:
    """画像ファイルをディスクから削除する"""
    path = IMAGES_DIR / filename
    if path.exists():
        path.unlink()


# ─── 一覧 ────────────────────────────────────────────────
@router.get("/")
def list_properties(
    request: Request,
    q: Optional[str] = None,
    accident_type: Optional[str] = None,
    confirm_status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Property)

    if q:
        like = f"%{q}%"
        query = query.filter(
            Property.address.like(like) |
            Property.summary.like(like) |
            Property.memo.like(like)
        )
    if accident_type:
        query = query.filter(Property.accident_type == accident_type)
    if confirm_status:
        query = query.filter(Property.confirm_status == confirm_status)

    properties = query.order_by(Property.created_at.desc()).all()

    return templates.TemplateResponse("list.html", {
        "request": request,
        "properties": properties,
        "accident_types": AccidentType,
        "confirm_statuses": ConfirmStatus,
        "q": q or "",
        "selected_accident_type": accident_type or "",
        "selected_confirm_status": confirm_status or "",
    })


# ─── 登録フォーム ────────────────────────────────────────
@router.get("/new")
def new_property_form(request: Request):
    return templates.TemplateResponse("form.html", {
        "request": request,
        "property": None,
        "accident_types": AccidentType,
        "confirm_statuses": ConfirmStatus,
        "action": "/new",
        "title": "物件登録",
    })


# ─── 登録処理 ────────────────────────────────────────────
@router.post("/new")
async def create_property(
    request: Request,
    address: str = Form(...),
    accident_type: str = Form(...),
    confirm_status: str = Form(...),
    summary: Optional[str] = Form(None),
    memo: Optional[str] = Form(None),
    map_url: Optional[str] = Form(None),
    images: list[UploadFile] = File(default=[]),
    db: Session = Depends(get_db),
):
    prop = Property(
        address=address,
        accident_type=accident_type,
        confirm_status=confirm_status,
        summary=summary or None,
        memo=memo or None,
        map_url=map_url or None,
    )
    db.add(prop)
    db.flush()  # IDを確定させる

    for img in images:
        if img.filename:
            filename = _save_image(img)
            db.add(PropertyImage(
                property_id=prop.id,
                filename=filename,
                original_filename=img.filename,
            ))

    db.commit()
    return RedirectResponse(url=f"/{prop.id}", status_code=303)


# ─── 詳細 ────────────────────────────────────────────────
@router.get("/{property_id}")
def detail_property(request: Request, property_id: int, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="物件が見つかりません")

    # GoogleマップURLをiframe埋め込み用に変換
    embed_url = _to_embed_url(prop.map_url)

    return templates.TemplateResponse("detail.html", {
        "request": request,
        "property": prop,
        "embed_url": embed_url,
    })


# ─── 編集フォーム ────────────────────────────────────────
@router.get("/{property_id}/edit")
def edit_property_form(request: Request, property_id: int, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="物件が見つかりません")

    return templates.TemplateResponse("form.html", {
        "request": request,
        "property": prop,
        "accident_types": AccidentType,
        "confirm_statuses": ConfirmStatus,
        "action": f"/{property_id}/edit",
        "title": "物件編集",
    })


# ─── 編集処理 ────────────────────────────────────────────
@router.post("/{property_id}/edit")
async def update_property(
    request: Request,
    property_id: int,
    address: str = Form(...),
    accident_type: str = Form(...),
    confirm_status: str = Form(...),
    summary: Optional[str] = Form(None),
    memo: Optional[str] = Form(None),
    map_url: Optional[str] = Form(None),
    images: list[UploadFile] = File(default=[]),
    db: Session = Depends(get_db),
):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="物件が見つかりません")

    prop.address = address
    prop.accident_type = accident_type
    prop.confirm_status = confirm_status
    prop.summary = summary or None
    prop.memo = memo or None
    prop.map_url = map_url or None

    for img in images:
        if img.filename:
            filename = _save_image(img)
            db.add(PropertyImage(
                property_id=prop.id,
                filename=filename,
                original_filename=img.filename,
            ))

    db.commit()
    return RedirectResponse(url=f"/{property_id}", status_code=303)


# ─── 画像削除 ────────────────────────────────────────────
@router.post("/{property_id}/images/{image_id}/delete")
def delete_image(property_id: int, image_id: int, db: Session = Depends(get_db)):
    img = db.query(PropertyImage).filter(PropertyImage.id == image_id).first()
    if img:
        _delete_image_file(img.filename)
        db.delete(img)
        db.commit()
    return RedirectResponse(url=f"/{property_id}/edit", status_code=303)


# ─── 削除処理 ────────────────────────────────────────────
@router.post("/{property_id}/delete")
def delete_property(property_id: int, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="物件が見つかりません")

    # 画像ファイルを物理削除
    for img in prop.images:
        _delete_image_file(img.filename)

    db.delete(prop)
    db.commit()
    return RedirectResponse(url="/", status_code=303)


# ─── ユーティリティ ──────────────────────────────────────
def _to_embed_url(url: Optional[str]) -> Optional[str]:
    """GoogleマップのURLをiframe埋め込み用URLに変換する。
    変換できない場合はNoneを返し、テンプレート側でリンク表示に切り替える。
    """
    if not url:
        return None

    # すでにembed形式ならそのまま返す
    if "google.com/maps/embed" in url:
        return url

    # @緯度,経度 を抽出（最も確実な方法）
    coord_match = re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+)", url)
    if coord_match:
        lat, lng = coord_match.group(1), coord_match.group(2)
        return f"https://maps.google.com/maps?q={lat},{lng}&output=embed"

    # q= パラメータがある場合
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    if "q" in params:
        q = params["q"][0]
        return f"https://maps.google.com/maps?q={q}&output=embed"

    # /maps/place/NAME/ 形式
    place_match = re.search(r"/maps/place/([^/@]+)", url)
    if place_match:
        place = place_match.group(1)
        return f"https://maps.google.com/maps?q={place}&output=embed"

    # 変換不可（goo.gl短縮URLなど）→ リンク表示にフォールバック
    return None
