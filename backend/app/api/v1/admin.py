from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...db import get_db
from ...services.overrides import upsert_override

router = APIRouter()

@router.post("/overrides")
def upsert(cele_jmeno_normalizovane: str, obdobi: int, id_poslanec: int, db: Session = Depends(get_db)):
    rec = upsert_override(db, cele_jmeno_normalizovane, obdobi, id_poslanec)
    return {"status":"ok", "id": rec.id}
