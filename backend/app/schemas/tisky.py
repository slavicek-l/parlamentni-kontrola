from pydantic import BaseModel
from typing import Optional

class TiskOut(BaseModel):
    id_tisk: int
    druh: Optional[str] = None
    nazev: Optional[str] = None
    stav_legislativni_faze: Optional[str] = None
    cislo_tisku: Optional[str] = None
    obdobi: Optional[int] = None
    datum_rozsahu_od: Optional[str] = None
