from sqlalchemy.orm import Session
from .name_normalizer import normalize_name
from app.models.mapping import MapovaniNazvuNaPoslance
from app.models.poslanci import Poslanec
from rapidfuzz import process, fuzz

def map_proposer(session: Session, name: str, obdobi: int) -> tuple[int | None, float, str]:
    norm = normalize_name(name)
    manual = session.query(MapovaniNazvuNaPoslance).filter_by(
        cele_jmeno_normalizovane=norm, obdobi=obdobi
    ).first()
    if manual:
        return manual.id_poslanec, 1.0, "manual"

    candidates = session.query(Poslanec.id_poslanec, Poslanec.jmeno, Poslanec.prijmeni).all()
    mapping = {pid: f"{j} {p}" for (pid, j, p) in candidates}
    if not mapping:
        return None, 0.0, "nomatch"

    best = process.extractOne(
        name, list(mapping.values()), scorer=fuzz.token_sort_ratio
    )
    if best and best[1] >= 90:
        inv = {v:k for k,v in mapping.items()}
        return inv[best[0]], best[1]/100.0, "fuzzy"
    return None, (best[1]/100.0 if best else 0.0), "nomatch"
