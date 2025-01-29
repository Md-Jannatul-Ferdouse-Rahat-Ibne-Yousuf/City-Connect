from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import crud
from database import get_db

# Define templates for rendering HTML
templates = Jinja2Templates(directory="templates")

register_router = APIRouter()


@register_router.get("/register", response_class=HTMLResponse)
def register_form(request: Request, db: Session = Depends(get_db)):
    roles = crud.get_roles(db)  
    return templates.TemplateResponse(
        "register.html", {"request": request, "roles": roles}
    )


@register_router.post("/register")
def register_user(
    request:Request,
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    phone_number: str = Form(None),
    role_id: int = Form(...),
    license_number: str = Form(None),  
    experience_years: str = Form(None),
    db: Session = Depends(get_db),
):
    try:
        user = crud.create_user(
            db = db,
            username=username,
            password=password,
            email=email,
            phone_number=phone_number,
        )
        user_id = user["id"]  
        print(f"Role id: {role_id}")
        crud.assign_role(db, user_id, role_id)

        if role_id == 2:
            crud.create_customer(db, user_id)
        elif role_id == 3:
            crud.create_driver(db, user_id, license_number, experience_years)

        return templates.TemplateResponse(
        "index.html", {"request": request}
    )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
