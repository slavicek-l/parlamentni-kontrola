from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from ...db import get_db
from ...models.tisky import Tisk, TiskyPoslanci, RoleEnum
from ...schemas.tisky import TiskOut
from ...services.search import apply_fulltext_ilike
from ...services.pagination import paginate

router = APIRouter()

@router.get("", response_model=list[TiskOut])
def list_tisky(
    db: Session = Depends(get_db),
    od: str | None = None,
    do: str | None = None,
    druh: str | None = None,
    faze: str | None = None,
    q: str | None = None,
    limit: int = Query(20, le=100),
    offset: int = 0,
):
    query = db.query(Tisk)
    if od:
        query = query.filter(Tisk.datum_rozsahu_od >= od)
    if do:
        query = query.filter(Tisk.datum_rozsahu_od <= do)
    if druh:
        query = query.filter(Tisk.druh == druh)
    if faze:
        query = query.filter(Tisk.stav_legislativni_faze == faze)
    query = apply_fulltext_ilike(query, [Tisk.nazev], q)
    items, total = paginate(query, limit, offset)
    return items

@router.get("/{id}", response_model=TiskOut)
def get_tisk(id: int, db: Session = Depends(get_db)):
    t = db.query(Tisk).filter_by(id_tisk=id).first()
    if not t: raise HTTPException(404, "Tisk nenalezen")
    return t
