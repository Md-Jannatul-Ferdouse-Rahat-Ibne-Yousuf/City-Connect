from sqlalchemy.orm import Session
from sqlalchemy.sql import text   

def add_salary(
    db: Session,
    driver_id: int,
    year: int,
    month: str,
    hourly: float,
    hours_worked: int,
    salary: float
):
    insert_query = text("""
        INSERT INTO driver_salary (driver_id, year, month, hourly, hours_worked, salary)
        VALUES (:driver_id, :year, :month, :hourly, :hours_worked, :salary);
    """)
    select_query = text("""
        SELECT id, driver_id, year, month, hourly, hours_worked, salary
        FROM driver_salary WHERE id = LAST_INSERT_ID();
    """)


    db.execute(insert_query, {
        "driver_id": driver_id,
        "year": year,
        "month": month,
        "hourly": hourly,
        "hours_worked": hours_worked,
        "salary": salary
    })
        
    # Retrieve the last inserted salary record
    result = db.execute(select_query)
    inserted_salary_record = result.fetchone()
    db.commit()

    return dict(inserted_salary_record._mapping)  

def get_driver_salary(db: Session, driver_id: int):
    query = text("""
        SELECT 
            s.driver_id,
            s.id,
            s.salary,
            s.year,
            s.month,
            s.hourly,
            s.hours_worked
        FROM driver_salary s
        WHERE s.driver_id = :driver_id
    """)
    result = db.execute(query, {"driver_id": driver_id}).fetchall()
    return [dict(row._mapping) for row in result] if result else []

def get_salary_record(db: Session, salary_id: int):
    query = text("SELECT id, driver_id, year, month, hourly, hours_worked, salary FROM driver_salary WHERE id = :salary_id LIMIT 1")
    result = db.execute(query, {"salary_id": salary_id})
    return result.fetchone()

def update_salary(
    db: Session,
    salary_id: int,
    year: int,
    month: str,
    hourly: float,
    hours_worked: int,
    salary: float
):
    driver_query = text("SELECT driver_id FROM driver_salary WHERE id = :salary_id")
    driver_result = db.execute(driver_query, {"salary_id": salary_id}).fetchone()

    if not driver_result:
        return None
    
    query = text("""
        UPDATE driver_salary
        SET year = :year, month = :month, hourly = :hourly, hours_worked = :hours_worked, salary = :salary
        WHERE id = :salary_id
    """)
    result = db.execute(query, {
        "salary_id": salary_id,
        "year": year,
        "month": month,
        "hourly": hourly,
        "hours_worked": hours_worked,
        "salary": salary
    })
    db.commit()
    return driver_result.driver_id
