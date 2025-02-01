from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import crud
from database import get_db
from utils import *

# Define templates for rendering HTML
templates = Jinja2Templates(directory="templates")

station_router = APIRouter()

@station_router.get("/stations", response_class=HTMLResponse)
async def get_stations(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageStations"))):
    try:
        user = crud.get_user_by_username(db, current_user["username"])
        user_id = user["id"]
        
        # Fetch roles of the current user
        roles = crud.get_user_roles(db, user_id)
        role_names = [role['name'] for role in roles]
        stations = crud.get_stations(db)
        return templates.TemplateResponse("stations.html", {"request": request, "stations": stations, "current_user": user, "role_names": role_names})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@station_router.get("/stations/new", response_class=HTMLResponse)
async def create_station(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageStations"))):
    user = crud.get_user_by_username(db, current_user["username"])
    user_id = user["id"]
    
    # Fetch roles of the current user
    roles = crud.get_user_roles(db, user_id)
    role_names = [role['name'] for role in roles]
    return templates.TemplateResponse("create_station.html", {"request": request, "current_user": user, "role_names": role_names})

@station_router.post("/stations/new")
async def create_station(
    name: str = Form(...), 
    db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageStations"))
):
    try:
        crud.create_station(db, name)
        return RedirectResponse(url=f"/stations?message=station created successfully!", status_code=303)

    except Exception as e:
        return RedirectResponse(url=f"/stations?error={str(e)}", status_code=303)
    

@station_router.get("/stations/{station_id}/edit", response_class=HTMLResponse)
async def edit_station(
    station_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_permission("ManageStations"))
):
    try:
        station = crud.get_station_by_id(db, station_id)
        if not station:
            raise HTTPException(status_code=404, detail="station not found")
        return templates.TemplateResponse(
            "edit_station.html", {"request": request, "station": station}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@station_router.post("/stations/{station_id}/edit")
async def update_station(
    station_id: int,
    name: str = Form(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_permission("ManageStations"))
):
    try:
        updated_station = crud.update_station(db, station_id, name)
        if not updated_station:
            raise HTTPException(status_code=404, detail="Station not found")
        return RedirectResponse(
            url=f"/stations?message=Station updated successfully!", status_code=303
        )
    except Exception as e:
        return RedirectResponse(
            url=f"/stations?error={str(e)}", status_code=303
        )


@station_router.get("/stops", response_class=HTMLResponse)
async def get_stations(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageStations"))):
    try:
        stops = crud.get_stops(db)
        user = crud.get_user_by_username(db, current_user["username"])
        user_id = user["id"]
        
        # Fetch roles of the current user
        roles = crud.get_user_roles(db, user_id)
        role_names = [role['name'] for role in roles]
        return templates.TemplateResponse("stops.html", {"request": request, "stops": stops, "current_user": user, "role_names": role_names})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@station_router.get("/stops/new", response_class=HTMLResponse)
async def create_station(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageStations"))):
    
    stations = crud.get_stations(db)
    routes = crud.get_routes(db)
    user = crud.get_user_by_username(db, current_user["username"])
    user_id = user["id"]
    
    # Fetch roles of the current user
    roles = crud.get_user_roles(db, user_id)
    role_names = [role['name'] for role in roles]
    return templates.TemplateResponse("create_stop.html", {"request": request, 
                                                           "routes": routes, 
                                                           "stations": stations, 
                                                           "current_user": user, 
                                                           "role_names": role_names})

@station_router.post("/stops/new")
async def create_station(
    route_id: int = Form(...), station_id: int = Form(...), stop_number: int = Form(...),
    db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageStations"))
):
    try:
        crud.create_stop(db, route_id, station_id, stop_number)
        return RedirectResponse(url=f"/stops?message=stop created successfully!", status_code=303)

    except Exception as e:
        return RedirectResponse(url=f"/stops?error={str(e)}", status_code=303)