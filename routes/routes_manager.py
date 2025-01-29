from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import crud
from database import get_db
from utils import *

# Define templates for rendering HTML
templates = Jinja2Templates(directory="templates")
route_router = APIRouter()

@route_router.get("/routes", response_class=HTMLResponse)
async def get_routes(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageRoutes"))):
    try:
        routes = crud.get_routes(db)
        return templates.TemplateResponse("routes.html", {"request": request, "routes": routes})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@route_router.get("/routes/new", response_class=HTMLResponse)
async def create_route(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageRoutes"))):
    stations = crud.get_stations(db)
    return templates.TemplateResponse("create_route.html", {"request": request, "stations": stations})

@route_router.post("/routes/new")
async def create_route(
    route_name: str = Form(...), origin_id: int = Form(...), destination_id: int = Form(...),
    db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageRoutes"))
):
    try:
        crud.create_route(db, route_name, origin_id, destination_id)
        return RedirectResponse(url=f"/routes?message=Route created successfully!", status_code=303)

    except Exception as e:
        return RedirectResponse(url=f"/routes?error={str(e)}", status_code=303)
    

@route_router.get("/routes/{route_id}/edit", response_class=HTMLResponse)
async def edit_route(
    route_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_permission("ManageRoutes"))
):
    try:
        route = crud.get_route_by_id(db, route_id)
        if not route:
            raise HTTPException(status_code=404, detail="route not found")
        return templates.TemplateResponse(
            "edit_route.html", {"request": request, "route": route}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@route_router.post("/routes/{route_id}/edit")
async def update_route(
    route_id: int,
    make: str = Form(...),
    model: str = Form(...),
    year: int = Form(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_permission("ManageRoutes"))
):
    try:
        updated_route = crud.update_route(db, route_id, make, model, year)
        if not updated_route:
            raise HTTPException(status_code=404, detail="route not found")
        return RedirectResponse(
            url=f"/routes?message=route updated successfully!", status_code=303
        )
    except Exception as e:
        return RedirectResponse(
            url=f"/routes?error={str(e)}", status_code=303
        )

@route_router.get("/timetables", response_class=HTMLResponse)
async def get_timetables(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageRoutes"))):
    try:
        timetables = crud.get_timetables(db)
        return templates.TemplateResponse("timetables.html", {"request": request, "timetables": timetables})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@route_router.get("/timetables/new", response_class=HTMLResponse)
async def create_timetable(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageRoutes"))):
    routes = crud.get_routes(db)
    stations = crud.get_stations(db)
    buses = crud.get_buses(db)
    drivers = crud.get_drivers(db)
    return templates.TemplateResponse("create_timetable.html", {"request": request, 
                                                            "stations": stations,
                                                            "routes": routes,
                                                            "drivers": drivers,
                                                            "buses": buses})

@route_router.post("/timetables/new")
async def create_timetable(
    route_id: int = Form(...), 
    bus_id: int = Form(...), driver_id: int = Form(...),
    station_id: int = Form(...), scheduled_time: str = Form(...),
    db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageRoutes"))
):
    try:
        crud.create_timetable(db, route_id, bus_id, driver_id, station_id, scheduled_time)
        return RedirectResponse(url=f"/timetables?message=Timetable created successfully!", status_code=303)

    except Exception as e:
        return RedirectResponse(url=f"/timetables?error={str(e)}", status_code=303)
    