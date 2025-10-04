from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.poslanci import Poslanec
from app.models.tisky import Tisk, TiskyPoslanci, RoleEnum
from app.models.hlasovani import Hlasovani, HlasovaniPoslancu, HlasVysledekEnum
import datetime

def run():
    db: Session = SessionLocal()
    if db.query(Poslanec).count() > 0:
        db.close()
        return
    p1 = Poslanec(id_poslanec=1, jmeno="Jan", prijmeni="Novák", strana="STR", kraj="KH", aktivni=True)
    p2 = Poslanec(id_poslanec=2, jmeno="Eva", prijmeni="Svobodová", strana="LIB", kraj="PHA", aktivni=True)
    db.add_all([p1,p2])
    t1 = Tisk(id_tisk=100, druh="zákon", nazev="Návrh zákona A", cislo_tisku="100", obdobi=9, datum_rozsahu_od=datetime.date(2024,1,10))
    t2 = Tisk(id_tisk=101, druh="novela", nazev="Novela zákona B", cislo_tisku="101", obdobi=9, datum_rozsahu_od=datetime.date(2024,3,5))
    db.add_all([t1,t2])
    db.add_all([
        TiskyPoslanci(id_tisk=100, id_poslanec=1, role=RoleEnum.navrhovatel),
        TiskyPoslanci(id_tisk=101, id_poslanec=1, role=RoleEnum.spolu_navrhovatel),
        TiskyPoslanci(id_tisk=101, id_poslanec=2, role=RoleEnum.navrhovatel),
    ])
    h1 = Hlasovani(id_hlasovani=500, schuze=1, cislo=1, datum=datetime.date(2024,1,10), nazev_kratky="Hlasování A", pro=80, proti=30, zdrzel=5, nehlasoval=5)
    db.add(h1)
    db.add_all([
        HlasovaniPoslancu(id_poslanec=1, id_hlasovani=500, vysledek=HlasVysledekEnum.A),
        HlasovaniPoslancu(id_poslanec=2, id_hlasovani=500, vysledek=HlasVysledekEnum.NP),
    ])
    db.commit()
    db.close()

if __name__ == "__main__":
    run()
