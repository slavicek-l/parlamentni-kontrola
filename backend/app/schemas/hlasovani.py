from pydantic import BaseModel
from typing import Optional, List

class HlasovaniOut(BaseModel):
    id_hlasovani: int
    datum: str
    nazev_kratky: Optional[str] = None
    vysledek: Optional[str] = None

class HlasovaniVysledky(BaseModel):
    id_hlasovani: int
    pro: int | None
    proti: int | None
    zdrzel: int | None
    nehlasoval: int | None
