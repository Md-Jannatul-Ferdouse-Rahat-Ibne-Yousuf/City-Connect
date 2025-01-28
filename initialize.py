from database import engine
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import Depends
import crud
from database import get_db, create_tables, SessionLocal

def initialize_roles(db: Session = Depends(get_db)):
    roles = [
        {"name": "Admin", "description": "Full access to all resources and management"},
        {"name": "Customer", "description": "Can view their own data"},
        {"name": "Driver", "description": "Can view their own salary and timetable"},
        {"name": "HR Manager", "description": "Manage driver salaries and details"},
        {"name": "Fleet Manager", "description": "Manage bus fleet and maintenance schedules"},
        {"name": "Route Manager", "description": "Manage routes and timetables"},
        {"name": "Station Manager", "description": "Manage station and route stops"},
    ]
    
    try:
        for role in roles:
            name = role["name"]
            description = role["description"]
            print(f"The name of the role: {name}")
            result = db.execute(
                text("INSERT INTO roles (name, description) VALUES (:name, :description)"), 
                {"name": name, "description": description}
            )
        db.commit()
    except:
        print(f"Error occurred")
    else:
        print("Roles initialized successfully.")


def initialize_permissions(db: Session = Depends(get_db)):
    permissions = [
        {"name": "FullAccess", "description": "Full access to all tables and management"},
        {"name": "ViewCustomerDetails", "description": "View their own customer details"},
        {"name": "ViewDriverSalary", "description": "View driver salary details"},
        {"name": "ViewTimetable", "description": "View driver timetable"},
        {"name": "EditDriverSalary", "description": "Edit driver salary details"},
        {"name": "ManageDrivers", "description": "Add, update, delete drivers"},
        {"name": "ManageBusFleet", "description": "Manage bus fleet and maintenance schedules"},
        {"name": "ManageRoutes", "description": "Add, update routes and stops"},
        {"name": "ManageStations", "description": "Add, update stations"},
        {"name": "ManageRolesPermissions", "description": "Manage roles and permissions"},
        {"name": "AddUsers", "description": "Add users and assign roles"},
    ]
    
    try:
        for permission in permissions:
            db.execute(text("INSERT INTO permissions (name, description) VALUES (:name, :description)"), permission)
        db.commit()
    except:
        print(f"Error occurred")
    else:
        print(f"Permission added successfully.")
    

def initialize_role_to_permission(db: Session = Depends(get_db)):
    try:
        db.execute(text("INSERT INTO role_permission (role_id, permission_id) VALUES "
                            "(1, 1), (1, 10), (1, 11), (2, 2), (3, 3), (4, 4), (4, 5), (4, 6), (5, 7), (6, 8), (7, 9)"))
        db.commit()
    except:
        print(f"Error occurred")
    else:
        print(f"Role-Permission mapped successfuly ")
    

def create_initial_admin_user(db: Session):
    username = "admin"  
    password = "admin"  
    email = "admin@example.com"  
    phone_number = "+880000"
    
    existing_user = crud.get_user_by_username(db, username)
    
    print(f"Existing user: {existing_user}")
    if not existing_user:
        crud.create_user(db, username, password, email, phone_number)
        print("Admin user created successfully.")
        return True
    else:
        print("Admin user already exists.")
        return False

def assign_admin_role_to_user(db: Session):
    username = "admin"
    user = crud.get_user_by_username(db, username)
    
    if user:
        user_id = user["id"]
        admin_role_id = crud.get_roles(db)[0]["id"]  
        crud.assign_role(db, user_id, admin_role_id)
        print("Admin role assigned to the initial admin user.")
    else:
        print("Admin user not found, cannot assign admin role.")
        

def run_initializers():
    db = SessionLocal()
    create_tables(db)
    initialize_roles(db)
    initialize_permissions(db)
    initialize_role_to_permission(db)
    res = create_initial_admin_user(db)
    if res:
        assign_admin_role_to_user(db)