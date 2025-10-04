from sqlalchemy.orm import Session
from sqlalchemy import func, case, literal
from app.models.tisky import Tisk, TiskyPoslanci, RoleEnum
from app.models.hlasovani import Hlasovani, HlasovaniPoslancu
from app.models.poslanci import Poslanec

def top_n_navrhovatele(session: Session, od: str | None, do: str | None, limit: int = 10):
    q = session.query(
        TiskyPoslanci.id_poslanec,
        func.sum(case((TiskyPoslanci.role == RoleEnum.navrhovatel, 1), else_=0)).label("navrhovatel"),
        func.sum(case((TiskyPoslanci.role == RoleEnum.spolu_navrhovatel, 1), else_=0)).label("spolu"),
        func.count().label("total"),
    ).join(Tisk, Tisk.id_tisk == TiskyPoslanci.id_tisk)

    if od:
        q = q.filter(Tisk.datum_rozsahu_od >= od)
    if do:
        q = q.filter(Tisk.datum_rozsahu_od <= do)

    q = q.group_by(TiskyPoslanci.id_poslanec).order_by(func.count().desc()).limit(limit)
    return q.all()
