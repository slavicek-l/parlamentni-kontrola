from pydantic import BaseModel
from typing import Optional

class PoslanecOut(BaseModel):
    id_poslanec: int
    jmeno: str
    prijmeni: str
    strana: Optional[str] = None
    kraj: Optional[str] = None
    foto_url: Optional[str] = None
    aktivni: bool

class PoslanecDetail(PoslanecOut):
    datum_narozeni: Optional[str] = None
    kontakty: Optional[str] = None
    aktivni_od: Optional[str] = None
    aktivni_do: Optional[str] = None
