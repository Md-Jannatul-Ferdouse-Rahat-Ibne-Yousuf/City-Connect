from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError

def get_stations(db: Session):
    query = text("""
        SELECT *
        FROM stations
    """)
    result = db.execute(query)
    return [dict(row) for row in result.mappings()] if result else []

def create_station(db: Session, name: str):

    insert_station_query = text("""
        INSERT INTO stations (name)
        VALUES (:name)
    """)

    db.execute(insert_station_query, {
        "name": name
    })

    db.commit()

def get_station_by_id(db: Session, station_id: int):
    query = text("""
                 SELECT id, name
                 FROM stations
                 WHERE id = :station_id
                 """)
    result = db.execute(query, {"station_id": station_id}).mappings().first()
    return dict(result) if result else None

def update_station(db: Session, station_id: int, name: str):
    query = text("""
        UPDATE stations
        SET name = :name
        WHERE id = :station_id
    """)
    result = db.execute(query, {"station_id": station_id, "name": name})
    db.commit()
    return result.rowcount > 0