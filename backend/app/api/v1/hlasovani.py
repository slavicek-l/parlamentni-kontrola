from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ...db import get_db
from ...models.hlasovani import Hlasovani, HlasovaniPoslancu
from ...schemas.hlasovani import HlasovaniOut, HlasovaniVysledky
from ...services.search import apply_fulltext_ilike
from ...services.pagination import paginate

router = APIRouter()

@router.get("", response_model=list[HlasovaniOut])
def list_hlasovani(
    db: Session = Depends(get_db),
    od: str | None = None,
    do: str | None = None,
    tema: int | None = None,
    vysledek: str | None = None,
    q: str | None = None,
    limit: int = Query(20, le=100),
    offset: int = 0,
):
    query = db.query(Hlasovani)
    if od:
        query = query.filter(Hlasovani.datum >= od)
    if do:
        query = query.filter(Hlasovani.datum <= do)
    query = apply_fulltext_ilike(query, [Hlasovani.nazev_kratky, Hlasovani.nazev_dlouhy], q)
    items, total = paginate(query, limit, offset)
    return items

@router.get("/{id}", response_model=HlasovaniOut)
def get_hlasovani(id: int, db: Session = Depends(get_db)):
    h = db.query(Hlasovani).filter_by(id_hlasovani=id).first()
    if not h:
        raise HTTPException(404, "Hlasování nenalezeno")
    return h

@router.get("/{id}/vysledky", response_model=HlasovaniVysledky)
def get_vysledky(id: int, db: Session = Depends(get_db)):
    h = db.query(Hlasovani).filter_by(id_hlasovani=id).first()
    if not h:
        raise HTTPException(404, "Hlasování nenalezeno")
    return HlasovaniVysledky(
        id_hlasovani=h.id_hlasovani,
        pro=h.pro, proti=h.proti, zdrzel=h.zdrzel, nehlasoval=h.nehlasoval
    )
