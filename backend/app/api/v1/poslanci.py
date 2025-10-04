from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from ...db import get_db
from ...models.poslanci import Poslanec
from ...services.search import apply_fulltext_ilike
from ...services.pagination import paginate
from ...schemas.poslanci import PoslanecOut, PoslanecDetail

router = APIRouter()

@router.get("", response_model=list[PoslanecOut])
def list_poslanci(
    db: Session = Depends(get_db),
    strana: str | None = None,
    kraj: str | None = None,
    aktivni: bool | None = None,
    q: str | None = None,
    limit: int = Query(20, le=100),
    offset: int = 0,
):
    query = db.query(Poslanec)
    if strana:
        query = query.filter(Poslanec.strana == strana)
    if kraj:
        query = query.filter(Poslanec.kraj == kraj)
    if aktivni is not None:
        query = query.filter(Poslanec.aktivni == aktivni)
    query = apply_fulltext_ilike(query, [Poslanec.jmeno, Poslanec.prijmeni, Poslanec.strana], q)
    items, total = paginate(query, limit, offset)
    return items

@router.get("/{id}", response_model=PoslanecDetail)
def get_poslanec(id: int, db: Session = Depends(get_db)):
    p = db.query(Poslanec).filter_by(id_poslanec=id).first()
    if not p:
        raise HTTPException(404, "Poslanec nenalezen")
    return p
