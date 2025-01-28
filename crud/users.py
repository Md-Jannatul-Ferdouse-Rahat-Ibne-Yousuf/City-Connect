from sqlalchemy.orm import Session
from sqlalchemy.sql import text

def create_user(db: Session, username: str, password: str, email: str, phone_number: str = None):
    insert_query = text("""
        INSERT INTO users (username, password, email, phone_number) 
        VALUES (:username, :password, :email, :phone_number)
    """)
    select_query = text("""
        SELECT id, username, email, phone_number, created_at, is_active 
        FROM users WHERE id = LAST_INSERT_ID()
    """)

    db.execute(insert_query, {
        "username": username,
        "password": password,
        "email": email,
        "phone_number": phone_number
    })

    result = db.execute(select_query)
    user = result.fetchone()

    db.commit()

    return dict(user._mapping) if user else None

def get_users(db: Session):
    query = text("SELECT * FROM users")
    result = db.execute(query)
    return [dict(row) for row in result.mappings()]

def get_user_by_username(db: Session, username: str):
    query = text("SELECT * FROM users WHERE username = :username")
    result = db.execute(query, {"username": username}).fetchone()
    return dict(result._mapping) if result else None

def get_user_roles(db: Session, user_id):
    query = text("""
        SELECT r.id, r.name, r.description
        FROM roles r
        JOIN user_role ur ON r.id = ur.role_id
        WHERE ur.user_id = :user_id
    """)
    result = db.execute(query, {"user_id": user_id})
    return [dict(row) for row in result.mappings()]

def get_user_permissions(db: Session, user_id):
    query = text("""
        SELECT DISTINCT p.name AS permission_name
        FROM permissions p
        JOIN role_permission rp ON p.id = rp.permission_id
        JOIN user_role ur ON rp.role_id = ur.role_id
        WHERE ur.user_id = :user_id
    """)
    result = db.execute(query, {"user_id": user_id})
    permissions = [row["permission_name"] for row in result.mappings()]
    return permissions

def has_permission(db: Session, user_id: int, permission_name: str):
    query = text("""
        SELECT COUNT(*) 
        FROM permissions up
        JOIN permissions p ON up.id = p.id
        WHERE up.id = :user_id AND p.name = :permission_name
    """)
    result = db.execute(query, {"user_id": user_id, "permission_name": permission_name})
    print(f"Res: {result}")
    count = result.scalar()
    return count > 0