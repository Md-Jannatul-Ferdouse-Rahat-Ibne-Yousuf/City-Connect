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
        LEFT JOIN bus b ON m.bus_id = b.id
    """)
    result = db.execute(query)
    return [dict(row) for row in result.mappings()] if result else []

def create_maintenance(db: Session, bus_id: str, date: str):

    insert_maintenance_query = text("""
        INSERT INTO maintenance (bus_id, date)
        VALUES (:bus_id, :date)
    """)

    db.execute(insert_maintenance_query, {
        "bus_id": bus_id,
        "date": date
    })

    db.commit()

def get_maintenance_by_id(db: Session, maintenance_id: int):
    query = text("""
                 SELECT id, bus_id, date
                 FROM maintenance
                 WHERE id = :maintenance_id
                 """)
    result = db.execute(query, {"maintenance_id": maintenance_id}).mappings().first()
    return dict(result) if result else None

def update_maintenance(db: Session, maintenance_id: int, bus_id: str, date: str):
    query = text("""
        UPDATE maintenance
        SET bus_id = :bus_id, date = :date
        WHERE id = :maintenance_id
    """)
    result = db.execute(query, {"maintenance_id": maintenance_id, "bus_id": bus_id, "date": date})
    db.commit()
    return result.rowcount > 0