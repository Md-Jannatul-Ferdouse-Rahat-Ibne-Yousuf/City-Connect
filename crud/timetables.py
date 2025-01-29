from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError

def get_timetables(db: Session):
    query = text("""
        SELECT 
            t.id,
            t.route_id,
            t.bus_id,
            t.driver_id,
            t.station_id,
            t.scheduled_time,
            r.name AS route_name,
            u.username AS driver_name,
            b.model AS bus_name,
            s.name AS station_name
        FROM timetables t
        INNER JOIN routes r ON t.route_id = r.id
        INNER JOIN users u ON t.driver_id = u.id
        INNER JOIN bus b ON t.bus_id = b.id
        INNER JOIN stations s ON t.station_id = s.id            
    """)
    result = db.execute(query)
    return [dict(row) for row in result.mappings()] if result else []

def create_timetable(db: Session, route_id: int, 
                     bus_id: int, driver_id: int, 
                     station_id: int, scheduled_time: str):

    insert_station_query = text("""
        INSERT INTO timetables (route_id, bus_id, driver_id, station_id, scheduled_time)
        VALUES (:route_id, :bus_id, :driver_id, :station_id, :scheduled_time)
    """)

    db.execute(insert_station_query, {
        "route_id": route_id,
        "bus_id": bus_id,
        "driver_id": driver_id,
        "station_id": station_id,
        "scheduled_time": scheduled_time 
    })

    db.commit()