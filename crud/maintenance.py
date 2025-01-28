from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError

def get_maintenance(db: Session):
    query = text("""
        SELECT 
                 m.id,
                 m.bus_id,
                 b.model,
                 b.make,
                 b.year,
                 m.date
        FROM maintenance m
        INNER JOIN bus b ON m.bus_id = b.id
    """)
    result = db.execute(query)
    return [dict(row) for row in result.mappings()] if result else []