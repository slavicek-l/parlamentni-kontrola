def paginate(query, limit: int, offset: int):
    total = query.count()
    items = query.limit(limit).offset(offset).all()
    return items, total
