from sqlalchemy.orm import Session
from app.models.mapping import MapovaniNazvuNaPoslance

def upsert_override(session: Session, cele_jmeno_normalizovane: str, obdobi: int, id_poslanec: int):
    rec = session.query(MapovaniNazvuNaPoslance).filter_by(
        cele_jmeno_normalizovane=cele_jmeno_normalizovane, obdobi=obdobi
    ).first()
    if rec:
        rec.id_poslanec = id_poslanec
    else:
        rec = MapovaniNazvuNaPoslance(
            cele_jmeno_normalizovane=cele_jmeno_normalizovane,
            obdobi=obdobi,
            id_poslanec=id_poslanec,
            zdroj="manual"
        )
        session.add(rec)
    session.commit()
    return rec
