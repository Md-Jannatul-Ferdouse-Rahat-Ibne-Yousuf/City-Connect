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

@home_router.get("/view_stops/{route_id}", response_class=HTMLResponse)
def view_route(request: Request, route_id: int, db: Session = Depends(get_db)):
    username = request.session.get("username")  
    stops = crud.get_stops_by_route_id(db, route_id)
    route = crud.get_route_by_id(db, route_id)
    return templates.TemplateResponse(
        "view_stops.html",  
        {"request": request, "username": username, "stops": stops, "route": route}
    )


@home_router.get("/view_timetables/{route_id}", response_class=HTMLResponse)
def view_timetables(request: Request, route_id:int, db: Session = Depends(get_db)):
    username = request.session.get("username")  
    timetables = crud.get_timetable_by_route_id(db, route_id)
    route = crud.get_route_by_id(db, route_id)
    return templates.TemplateResponse(
        "view_timetables.html", {"request": request, "username": username, "timetables": timetables, "route": route}
    )