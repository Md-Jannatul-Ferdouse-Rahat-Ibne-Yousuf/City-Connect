from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import crud
from database import get_db
from utils import *

# Define templates for rendering HTML
templates = Jinja2Templates(directory="templates")

driver_router = APIRouter()

@driver_router.get("/timetables/driver/{driver_id}", response_class=HTMLResponse)
async def get_driver_timetables(request: Request, driver_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Call the function to get timetables by driver_id
    timetables = crud.get_timetables_by_driver_id(db, driver_id)
    user = crud.get_user_by_username(db, current_user["username"])
    user_id = user["id"]
    
    # Fetch roles of the current user
    roles = crud.get_user_roles(db, user_id)
    role_names = [role['name'] for role in roles]
    # Render the timetables in an HTML template
    return templates.TemplateResponse("driver_timetables.html", {"request": request, "timetables": timetables, "user_id": user_id, "current_user": user, "role_names": role_names})
