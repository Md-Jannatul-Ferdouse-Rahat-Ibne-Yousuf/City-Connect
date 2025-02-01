from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from fastapi import Depends
from dotenv import load_dotenv

load_dotenv()

import os

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Raw SQL table creation queries
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(250) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(15),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active ENUM('Y', 'N') DEFAULT 'Y'
);
"""

create_roles_table = """
CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(250) UNIQUE NOT NULL,
    description VARCHAR(255)
);
"""

create_permissions_table = """
CREATE TABLE IF NOT EXISTS permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(250) UNIQUE NOT NULL,
    description VARCHAR(255)
);
"""

create_user_role_table = """
CREATE TABLE IF NOT EXISTS user_role (
    user_id INT,
    role_id INT,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);
"""

create_role_permission_table = """
CREATE TABLE IF NOT EXISTS role_permission (
    role_id INT,
    permission_id INT,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE
);
"""

create_drivers_table = """
CREATE TABLE IF NOT EXISTS drivers (
    id INT PRIMARY KEY,
    license_number VARCHAR(20) UNIQUE NOT NULL,
    experience_years INT NOT NULL,
    FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE
);
"""

create_customers_table = """
CREATE TABLE IF NOT EXISTS customers (
    id INT PRIMARY KEY,
    loyalty_points INT DEFAULT 0,
    FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE
);
"""

create_stations_table = """
CREATE TABLE IF NOT EXISTS stations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(250) NOT NULL
);
"""

create_routes_table = """
CREATE TABLE IF NOT EXISTS routes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(250) NOT NULL,
    origin_id INT NOT NULL,
    destination_id INT NOT NULL,
    FOREIGN KEY (origin_id) REFERENCES stations(id) ON DELETE CASCADE,
    FOREIGN KEY (destination_id) REFERENCES stations(id) ON DELETE CASCADE
);
"""

create_stops_table = """
CREATE TABLE IF NOT EXISTS stops (
    id INT AUTO_INCREMENT PRIMARY KEY,
    route_id INT NOT NULL,
    station_id INT NOT NULL,
    stop_number INT NOT NULL,
    FOREIGN KEY (route_id) REFERENCES routes(id) ON DELETE CASCADE,
    FOREIGN KEY (station_id) REFERENCES stations(id) ON DELETE CASCADE
);
"""


create_bus_table = """
CREATE TABLE IF NOT EXISTS bus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    make VARCHAR(250) NOT NULL,
    model VARCHAR(250) NOT NULL,
    year INT NOT NULL
);
"""

create_maintenance_table = """
CREATE TABLE IF NOT EXISTS maintenance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bus_id INT NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (bus_id) REFERENCES bus(id) ON DELETE CASCADE
);
"""


create_timetable_table = """
CREATE TABLE IF NOT EXISTS timetables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    route_id INT NOT NULL,
    bus_id INT NOT NULL,
    driver_id INT NOT NULL,
    station_id INT NOT NULL,
    scheduled_time DATETIME NOT NULL,
    FOREIGN KEY (route_id) REFERENCES routes(id) ON DELETE CASCADE,
    FOREIGN KEY (bus_id) REFERENCES bus(id) ON DELETE CASCADE,
    FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE CASCADE,
    FOREIGN KEY (station_id) REFERENCES stations(id) ON DELETE CASCADE
);
"""


create_driver_salary_table = """
CREATE TABLE IF NOT EXISTS driver_salary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT NOT NULL,
    month ENUM('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec') NOT NULL,
    driver_id INT NOT NULL,
    hourly DECIMAL(10, 2) NOT NULL,
    hours_worked INT NOT NULL,
    salary DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE CASCADE
);
"""


create_customer_history_table = """
CREATE TABLE IF NOT EXISTS customer_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    date_time DATETIME NOT NULL,
    enter_station_id INT NOT NULL,
    exit_station_id INT NOT NULL,
    charges DECIMAL(10, 2) NOT NULL,
    credits DECIMAL(10, 2) NOT NULL,
    balance DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    FOREIGN KEY (enter_station_id) REFERENCES stations(id) ON DELETE CASCADE,
    FOREIGN KEY (exit_station_id) REFERENCES stations(id) ON DELETE CASCADE
);
"""

def create_tables(db: Session):
    db.execute(text(create_users_table))
    db.execute(text(create_roles_table))
    db.execute(text(create_permissions_table))
    db.execute(text(create_user_role_table))
    db.execute(text(create_role_permission_table))
    db.execute(text(create_drivers_table))
    db.execute(text(create_customers_table))
    db.execute(text(create_stations_table))
    db.execute(text(create_routes_table))
    db.execute(text(create_stops_table))
    db.execute(text(create_stops_table))
    db.execute(text(create_bus_table))
    db.execute(text(create_maintenance_table))
    db.execute(text(create_timetable_table))
    db.execute(text(create_driver_salary_table))
    db.execute(text(create_customer_history_table))

    print("All tables created successfully!")
