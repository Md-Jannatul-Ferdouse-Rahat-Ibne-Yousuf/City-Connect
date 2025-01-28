from sqlalchemy.orm import Session
from sqlalchemy.sql import text

def create_customer(db: Session, user_id: int):
    loyalty_points = 0

    insert_customer_query = text("""
        INSERT INTO customers (id, loyalty_points)
        VALUES (:user_id, :loyalty_points)
    """)

    db.execute(insert_customer_query, {
        "user_id": user_id,
        "loyalty_points": loyalty_points
    })

    db.commit()
    