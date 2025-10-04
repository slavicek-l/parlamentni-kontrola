from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, case, text
from ...db import get_db
from ...models.tisky import Tisk, TiskyPoslanci, RoleEnum
from ...models.hlasovani import Hlasovani, HlasovaniPoslancu
from ...schemas.stats import UcastOut, NavrhySummaryItem

router = APIRouter()

@router.get("/navrhy/top")
def navrhy_top(
    db: Session = Depends(get_db),
    od: str | None = None,
    do: str | None = None,
    limit: int = 10,
):
    q = db.query(
        TiskyPoslanci.id_poslanec.label("id_poslanec"),
        func.sum(case((TiskyPoslanci.role == RoleEnum.navrhovatel, 1), else_=0)).label("navrhovatel"),
        func.sum(case((TiskyPoslanci.role == RoleEnum.spolu_navrhovatel, 1), else_=0)).label("spolu"),
        func.count().label("total"),
    ).join(Tisk, Tisk.id_tisk == TiskyPoslanci.id_tisk)
    if od:
        q = q.filter(Tisk.datum_rozsahu_od >= od)
    if do:
        q = q.filter(Tisk.datum_rozsahu_od <= do)
    q = q.group_by(TiskyPoslanci.id_poslanec).order_by(func.count().desc()).limit(limit)
    return [dict(id_poslanec=r.id_poslanec, navrhovatel=r.navrhovatel or 0, spolu=r.spolu or 0, total=r.total) for r in q.all()]

@router.get("/navrhy/trendy")
def navrhy_trendy(
    db: Session = Depends(get_db),
    od: str | None = None,
    do: str | None = None,
    bucket: str = Query("mesic", regex="^(mesic|ctvrtleti|rok)$"),
):
    trunc = {"mesic":"month", "ctvrtleti":"quarter", "rok":"year"}[bucket]
    q = db.query(
        TiskyPoslanci.id_poslanec,
        func.date_trunc(trunc, Tisk.datum_rozsahu_od).label("bucket"),
        func.count().label("total"),
    ).join(Tisk, Tisk.id_tisk == TiskyPoslanci.id_tisk)
    if od:
        q = q.filter(Tisk.datum_rozsahu_od >= od)
    if do:
        q = q.filter(Tisk.datum_rozsahu_od <= do)
    q = q.group_by(TiskyPoslanci.id_poslanec, func.date_trunc(trunc, Tisk.datum_rozsahu_od))
    return [dict(id_poslanec=r.id_poslanec, bucket=str(r.bucket.date()), total=r.total) for r in q.all()]

@router.get("/ucast")
def ucast(
    db: Session = Depends(get_db),
    obdobi: int | None = None,
    strana: str | None = None,
):
    q = db.query(
        HlasovaniPoslancu.id_poslanec,
        func.sum(case((HlasovaniPoslancu.vysledek == "NP", 1), else_=0)).label("nepritomen"),
        func.sum(case((HlasovaniPoslancu.vysledek != "NP", 1), else_=0)).label("pritomen"),
        func.count().label("total"),
        func.date_trunc("month", Hlasovani.datum).label("bucket"),
    ).join(Hlasovani, Hlasovani.id_hlasovani == HlasovaniPoslancu.id_hlasovani).group_by(
        HlasovaniPoslancu.id_poslanec, func.date_trunc("month", Hlasovani.datum)
    )
    return [dict(id_poslanec=r.id_poslanec, pritomen=int(r.pritomen), nepritomen=int(r.nepritomen), total=int(r.total), bucket=str(r.bucket.date())) for r in q.all()]
