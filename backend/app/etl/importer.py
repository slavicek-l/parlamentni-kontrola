import os, io, csv, datetime
from sqlalchemy.orm import Session
from ..config import settings
from .downloader import download_zip, extract_zip, sha256_bytes
from .unl_parser import detect_decode, parse_unl
from app.models.poslanci import Poslanec
from app.models.hlasovani import Hlasovani, HlasovaniPoslancu, HlasVysledekEnum
from app.models.tisky import Tisk, TiskyPoslanci, RoleEnum
from app.models.mapping import ImportAudit
from sqlalchemy import text

def upsert_poslanec(session: Session, row: list[str | None]):
    idp = int(row[0])
    rec = session.get(Poslanec, idp)
    if not rec:
        rec = Poslanec(id_poslanec=idp, jmeno=row[1] or "", prijmeni=row[2] or "")
        session.add(rec)
    rec.strana = row[3]
    rec.kraj = row[4]
    session.flush()

def upsert_hlasovani(session: Session, row: list[str | None]):
    idh = int(row[0])
    rec = session.get(Hlasovani, idh)
    if not rec:
        rec = Hlasovani(
            id_hlasovani=idh,
            schuze=int(row[1] or 0),
            cislo=int(row[2] or 0),
            datum=datetime.date.fromisoformat(row[3]) if row[3] else datetime.date.today(),
        )
        session.add(rec)
    rec.nazev_kratky = row[4]
    session.flush()

def upsert_hlasovani_poslancu(session: Session, row: list[str | None]):
    idp, idh = int(row[0]), int(row[1])
    vysl = (row[2] or "NP")
    rec = session.query(HlasovaniPoslancu).filter_by(id_poslanec=idp, id_hlasovani=idh).first()
    if not rec:
        rec = HlasovaniPoslancu(id_poslanec=idp, id_hlasovani=idh, vysledek=HlasVysledekEnum(vysl))
        session.add(rec)
    else:
        rec.vysledek = HlasVysledekEnum(vysl)
    session.flush()

def upsert_tisk(session: Session, row: list[str | None]):
    idt = int(row[0])
    rec = session.get(Tisk, idt)
    if not rec:
        rec = Tisk(id_tisk=idt)
        session.add(rec)
    rec.druh = row[1]
    rec.nazev = row[2]
    rec.cislo_tisku = row[3]
    rec.obdobi = int(row[4] or 0)
    rec.datum_rozsahu_od = datetime.date.fromisoformat(row[5]) if row[5] else None
    session.flush()

def upsert_tisky_poslanci(session: Session, row: list[str | None]):
    idt, idp = int(row[0]), int(row[1])
    role = row[2] or "navrhovatel"
    rec = session.query(TiskyPoslanci).filter_by(id_tisk=idt, id_poslanec=idp, role=RoleEnum(role)).first()
    if not rec:
        rec = TiskyPoslanci(id_tisk=idt, id_poslanec=idp, role=RoleEnum(role))
        session.add(rec)
    session.flush()

def idempotent_import(session: Session, zip_relpath: str, filename: str, handler):
    content = download_zip(zip_relpath)
    digest = sha256_bytes(content)
    exists = session.query(ImportAudit).filter_by(soubor=filename, hash=digest).first()
    if exists:
        return "unchanged"
    workdir = settings.ETL_WORK_DIR
    os.makedirs(workdir, exist_ok=True)
    extract_zip(content, workdir)
    with open(os.path.join(workdir, filename), "rb") as f:
        text = detect_decode(f.read())
    ok = fail = 0
    for parts in parse_unl(text):
        try:
            handler(session, parts)
            ok += 1
        except Exception:
            fail += 1
    session.add(ImportAudit(soubor=filename, hash=digest, verze="v1", zaznamenano=str(datetime.datetime.utcnow()), radku_ok=ok, radku_fail=fail))
    session.commit()
    return "imported"

def full_import(session: Session):
    idempotent_import(session, "psp_data/poslanci.zip", "poslanci.unl", upsert_poslanec)
    idempotent_import(session, "psp_data/hlasovani.zip", "hlasovani.unl", upsert_hlasovani)
    idempotent_import(session, "psp_data/hlasovani_poslanci.zip", "hlasovani_poslanci.unl", upsert_hlasovani_poslancu)
    idempotent_import(session, "psp_data/tisky.zip", "tisky.unl", upsert_tisk)
    idempotent_import(session, "psp_data/tisky_poslanci.zip", "tisky_poslanci.unl", upsert_tisky_poslanci)
