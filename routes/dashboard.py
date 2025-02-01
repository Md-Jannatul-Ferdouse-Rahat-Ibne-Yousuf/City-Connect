from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import crud
from database import get_db
from utils import *

# Define templates for rendering HTML
templates = Jinja2Templates(directory="templates")

dashboard_router = APIRouter()

@dashboard_router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user = crud.get_user_by_username(db, current_user["username"])
        user_id = user["id"]

        print(f"User: {user_id}")
        
        # Fetch roles of the current user
        roles = crud.get_user_roles(db, user_id)
        role_names = [role['name'] for role in roles]
        
        return templates.TemplateResponse("dashboard.html", {"request": request, "current_user": user, "user_id": user_id, "role_names": role_names})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))