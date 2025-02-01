from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import crud
from database import get_db
from utils import *


# Define templates for rendering HTML
templates = Jinja2Templates(directory="templates")

register_router = APIRouter()


@register_router.get("/register", response_class=HTMLResponse)
def register_form(request: Request, db: Session = Depends(get_db)):
    roles = crud.get_roles(db)  
    username = request.session.get("username") 
    permissions = ""
    if username:
        user = crud.get_user_by_username(db, username)
        user_id = user['id'] 
        permissions = crud.get_user_permissions(db, user_id)
    
    if username is not None and not ("FullAccess" in permissions or "ManageDrivers" in permissions):
        return RedirectResponse(url="/", status_code=303)

    
    return templates.TemplateResponse(
        "register.html", {"request": request, "roles": roles, "username": username, "permissions": permissions}
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
    current_user: dict = Depends(get_current_user)
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

        role_names = []
        try:
            user = crud.get_user_by_username(db, current_user["username"])
            user_id = user["id"]
            
            # Fetch roles of the current user
            roles = crud.get_user_roles(db, user_id)
            role_names = [role['name'] for role in roles]
        except:
            pass
        
        print(f"Curr: {current_user}")
        if current_user["username"]:
            return RedirectResponse(
                url=f"/dashboard?message=User%20created%20successfully",
                status_code=303
            )
        
        return templates.TemplateResponse(
        "login.html", {"request": request, "current_user": user, "role_names": role_names}
    )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
