from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError

def get_stops(db: Session):
    query = text("""
        SELECT 
                st.route_id,
                st.station_id,
                st.stop_number,
                s.name AS station_name,
                r.name AS route_name
        FROM stops st
        INNER JOIN stations s ON st.station_id = s.id
        INNER JOIN routes r ON st.route_id = r.id
                 
    """)
    result = db.execute(query)
    return [dict(row) for row in result.mappings()] if result else []

def create_stop(db: Session, route_id: int, station_id: int, stop_number: int):

    insert_station_query = text("""
        INSERT INTO stops (route_id, station_id, stop_number)
        VALUES (:route_id, :station_id, :stop_number)
    """)

    db.execute(insert_station_query, {
        "route_id": route_id,
        "station_id": station_id,
        "stop_number": stop_number
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