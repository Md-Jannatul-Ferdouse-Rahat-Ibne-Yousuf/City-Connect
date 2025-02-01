from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError

def get_routes(db: Session):
    query = text("""
        SELECT 
            r.id,
            r.name,
            r.origin_id,
            s1.name AS origin_name,
            r.destination_id,
            s2.name AS destination_name
        FROM routes r
        INNER JOIN stations s1 ON r.origin_id = s1.id
        INNER JOIN stations s2 ON r.destination_id = s2.id 

    """)
    result = db.execute(query)
    return [dict(row) for row in result.mappings()] if result else []

def create_route(db: Session, route_name: str, origin_id: int, destination_id: int):

    insert_station_query = text("""
        INSERT INTO routes (name, origin_id, destination_id)
        VALUES (:route_name, :origin_id, :destination_id)
    """)

    db.execute(insert_station_query, {
        "route_name": route_name,
        "origin_id": origin_id,
        "destination_id": destination_id
    })

    db.commit()

def get_route_by_id(db: Session, route_id: int):
    query = text("""
        SELECT 
            r.id,
            r.name,
            r.origin_id,
            s1.name AS origin_name,
            r.destination_id,
            s2.name AS destination_name
        FROM routes r
        INNER JOIN stations s1 ON r.origin_id = s1.id
        INNER JOIN stations s2 ON r.destination_id = s2.id
        WHERE r.id = :route_id
    """)

    result = db.execute(query, {"route_id": route_id}).mappings().first()
    return dict(result) if result else None
