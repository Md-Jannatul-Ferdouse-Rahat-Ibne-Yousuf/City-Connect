from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError

def get_buses(db: Session):
    query = text("""
        SELECT *
        FROM bus
    """)
    result = db.execute(query)
    return [dict(row) for row in result.mappings()] if result else []
    
def create_bus(db: Session, make: str, model: str, year: int):

    insert_bus_query = text("""
        INSERT INTO bus (make, model, year)
        VALUES (:make, :model, :year)
    """)

    db.execute(insert_bus_query, {
        "make": make,
        "model": model,
        "year": year
    })

    db.commit()

def get_bus_by_id(db: Session, bus_id: int):
    query = text("SELECT * FROM bus WHERE id = :bus_id")
    result = db.execute(query, {"bus_id": bus_id}).mappings().first()
    return dict(result) if result else None

def update_bus(db: Session, bus_id: int, make: str, model: str, year: int):
    query = text("""
        UPDATE bus
        SET make = :make, model = :model, year = :year
        WHERE id = :bus_id
    """)
    result = db.execute(query, {"bus_id": bus_id, "make": make, "model": model, "year": year})
    db.commit()
    return result.rowcount > 0
