from sqlalchemy.orm.query import Query
from database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
def apply_limit_offset(
    query: Query,
    limit: int | None = None,
    offset: int | None = None
) -> Query:
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset*limit)
    return query
