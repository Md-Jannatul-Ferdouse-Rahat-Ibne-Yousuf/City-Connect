from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import crud
from database import get_db
from utils import *

# Define templates for rendering HTML
templates = Jinja2Templates(directory="templates")

home_router = APIRouter()

@home_router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    username = request.session.get("username")  
    routes = crud.get_routes(db)
    return templates.TemplateResponse(
        "index.html", {"request": request, "username": username, "routes": routes}
    )