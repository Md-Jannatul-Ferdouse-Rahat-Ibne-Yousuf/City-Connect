from sqlalchemy.orm import Session
from sqlalchemy.sql import text

def create_role(db: Session, name: str, description: str):
    query = text("INSERT INTO roles (name, description) VALUES (:name, :description)")
    db.execute(query, {"name": name, "description": description})
    db.commit()

def create_permission(db: Session, name: str, description: str):
    query = text("INSERT INTO permissions (name, description) VALUES (:name, :description)")
    db.execute(query, {"name": name, "description": description})
    db.commit()

def get_roles(db: Session):
    query = text("SELECT id, name, description FROM roles")
    result = db.execute(query)
    return [dict(row) for row in result.mappings().all()]

def get_permissions(db: Session):
    query = text("SELECT id, name FROM permissions")
    result = db.execute(query)
    return [dict(row) for row in result.mappings()]

def assign_role(db: Session, user_id, role_id):
    query = text("""
        INSERT INTO user_role (user_id, role_id)
        VALUES (:user_id, :role_id)
    """)
    db.execute(query, {"user_id": user_id, "role_id": role_id})
    db.commit()
    return {"message": "Role assigned successfully"}

def get_role_permissions(db: Session, role_id):
    query = text("""
        SELECT p.id, p.name, p.description
        FROM permissions p
        JOIN role_permission rp ON p.id = rp.permission_id
        WHERE rp.role_id = :role_id
    """)
    result = db.execute(query, {"role_id": role_id})
    permissions = [dict(row) for row in result.mappings()]
    return permissions

def assign_permission_to_role(db: Session, role_id: int, permission_id: int):
    query = text("INSERT INTO role_permission (role_id, permission_id) VALUES (:role_id, :permission_id)")
    db.execute(query, {"role_id": role_id, "permission_id": permission_id})
    db.commit()