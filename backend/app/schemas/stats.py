from pydantic import BaseModel
from typing import List, Optional

class UcastOut(BaseModel):
    id_poslanec: int
    pritomen: int
    nepritomen: int
    total: int
    bucket: str

class NavrhySummaryItem(BaseModel):
    id_poslanec: int
    bucket: str
    navrhovatel_count: int
    spolu_count: int
    total: int
