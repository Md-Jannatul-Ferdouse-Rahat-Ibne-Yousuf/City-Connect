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
        stations = crud.get_stations(db)
        return templates.TemplateResponse("stations.html", {"request": request, "stations": stations})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@station_router.get("/stations/new", response_class=HTMLResponse)
async def create_station(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageStations"))):
    return templates.TemplateResponse("create_station.html", {"request": request})

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


@station_router.get("/route/stations", response_class=HTMLResponse)
async def get_router_stations(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageStations"))):
    try:
        router_stations = crud.get_router_stations(db)
        return templates.TemplateResponse("route_stations.html", {"request": request, "router_stations": router_stations})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@station_router.get("/route/stations/new", response_class=HTMLResponse)
async def create_route_station(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageStations"))):
    stations = crud.get_stations(db)
    return templates.TemplateResponse("create_route_station.html", {"request": request, "stations": stations})

@station_router.post("/route/stations/new")
async def create_station(
    name: str = Form(...), 
    db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageStations"))
):
    try:
        crud.create_station(db, name)
        return RedirectResponse(url=f"/stations?message=station created successfully!", status_code=303)

    except Exception as e:
        return RedirectResponse(url=f"/stations?error={str(e)}", status_code=303)