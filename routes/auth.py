from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
import crud
from fastapi.templating import Jinja2Templates

# Define templates for rendering HTML
templates = Jinja2Templates(directory="templates")

auth_router = APIRouter()

@auth_router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@auth_router.post("/login")
def login(
    username: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db), 
    request: Request = None
):

    user = crud.get_user_by_username(db, username)  # Fetch user from the database
    if not user or user["password"] != password:
        return RedirectResponse(url=f"/login?error=Incorrect Password or Username", status_code=303)
    
    user_id = user["id"]
    user_permissions = crud.get_user_permissions(db, user_id)
    user_roles = crud.get_user_roles(db, user_id)
    # Store user information in the session
    request.session["username"] = user["username"]
    request.session["role_names"] = [role["name"] for role in user_roles] if isinstance(user_roles, list) else user_roles.get("name")
    if isinstance(user_permissions, list):
        request.session["permissions"] = [perm["permission_name"] for perm in user_permissions if isinstance(perm, dict)]
    elif isinstance(user_permissions, dict):
        request.session["permissions"] = user_permissions.get("permission_name")
    else:
        request.session["permissions"] = []


    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@auth_router.get("/logout")
def logout(request: Request):

    request.session.clear()  # Clear session
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
