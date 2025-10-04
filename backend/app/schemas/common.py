from pydantic import BaseModel

class PageMeta(BaseModel):
    limit: int
    offset: int
    total: int
