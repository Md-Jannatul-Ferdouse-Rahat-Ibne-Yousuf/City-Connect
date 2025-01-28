from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError

def create_driver(db: Session, user_id: int, license_number: str, experience_years: int):
    query = text("""
        INSERT INTO drivers (id, license_number, experience_years)
        VALUES (:user_id, :license_number, :experience_years)
    """)
    db.execute(query, {"user_id": user_id, "license_number": license_number, "experience_years": experience_years})
    db.commit()

def get_drivers(db: Session):
    query = text("""
        SELECT 
            u.id AS user_id,
            u.username,
            u.email,
            u.phone_number,
            d.id AS driver_id,
            d.license_number,
            d.experience_years
        FROM drivers d
        INNER JOIN users u ON d.id = u.id
    """)
    result = db.execute(query)
    return [dict(row._mapping) for row in result] if result else []

def get_driver_by_id(db: Session, driver_id: int):
    query = text("""
        SELECT 
            u.id AS user_id,
            u.username,
            u.email,
            u.phone_number,
            d.id AS driver_id,
            d.license_number,
            d.experience_years
        FROM drivers d
        INNER JOIN users u ON d.id = u.id
        WHERE d.id = :driver_id
    """)
    result = db.execute(query, {"driver_id": driver_id}).fetchone() 
    return dict(result._mapping) if result else None


def update_driver(db: Session, driver_id: int, username: str, email: str, phone_number: str, license_number: str, experience_years: int):
    try:
        # Update `users` table
        user_query = text("""
            UPDATE users
            SET username = :username, email = :email, phone_number = :phone_number
            WHERE id = :driver_id
        """)
        db.execute(user_query, {
            "driver_id": driver_id,
            "username": username,
            "email": email,
            "phone_number": phone_number,
        })
        
        # Update `drivers` table
        driver_query = text("""
            UPDATE drivers
            SET license_number = :license_number, experience_years = :experience_years
            WHERE id = :driver_id
        """)
        db.execute(driver_query, {
            "driver_id": driver_id,
            "license_number": license_number,
            "experience_years": experience_years,
        })
        
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error updating driver: {e}")
        return False

def delete_driver(db: Session, driver_id: int):
    try:
        query = text("""
            DELETE FROM drivers WHERE id = :driver_id;
            DELETE FROM users WHERE id = :driver_id;
        """)
        db.execute(query, {"driver_id": driver_id})
        return True
    except Exception:
        return False
 


def get_driver_timetable(db: Session, driver_id: int):
    query = text("SELECT * FROM timetables WHERE driver_id = :driver_id")
    result = db.execute(query, {"driver_id": driver_id}).fetchall()
    return [dict(row._mapping) for row in result] if result else []