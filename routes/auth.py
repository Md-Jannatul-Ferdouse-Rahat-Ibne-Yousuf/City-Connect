from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from crud import get_user_by_username
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

    user = get_user_by_username(db, username)  # Fetch user from the database
    if not user or user["password"] != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )
    # Store user information in the session
    request.session["username"] = user["username"]
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@auth_router.get("/logout")
def logout(request: Request):

    request.session.clear()  # Clear session
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
