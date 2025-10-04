from sqlalchemy.orm import Query
from sqlalchemy import or_, func

def apply_fulltext_ilike(query: Query, columns, q: str | None):
    if q:
        ilikes = [col.ilike(f"%{q}%") for col in columns]
        return query.filter(or_(*ilikes))
    return query
