from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import crud
from database import get_db
from utils import *

# Define templates for rendering HTML
templates = Jinja2Templates(directory="templates")

fleet_router = APIRouter()

@fleet_router.get("/buses", response_class=HTMLResponse)
async def get_buses(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageBusFleet"))):
    try:
        buses = crud.get_buses(db)
        return templates.TemplateResponse("buses.html", {"request": request, "buses": buses})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@fleet_router.get("/buses/{bus_id}/edit", response_class=HTMLResponse)
async def edit_bus(
    bus_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_permission("ManageBusFleet"))
):
    try:
        bus = crud.get_bus_by_id(db, bus_id)
        if not bus:
            raise HTTPException(status_code=404, detail="Bus not found")
        return templates.TemplateResponse(
            "edit_bus.html", {"request": request, "bus": bus}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@fleet_router.post("/buses/{bus_id}/edit")
async def update_bus(
    bus_id: int,
    make: str = Form(...),
    model: str = Form(...),
    year: int = Form(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_permission("ManageBusFleet"))
):
    try:
        updated_bus = crud.update_bus(db, bus_id, make, model, year)
        if not updated_bus:
            raise HTTPException(status_code=404, detail="Bus not found")
        return RedirectResponse(
            url=f"/buses?message=Bus updated successfully!", status_code=303
        )
    except Exception as e:
        return RedirectResponse(
            url=f"/buses?error={str(e)}", status_code=303
        )


@fleet_router.get("/buses/new", response_class=HTMLResponse)
async def create_bus(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageBusFleet"))):
    return templates.TemplateResponse("add_bus.html", {"request": request})

@fleet_router.post("/buses/new")
async def create_bus(
    make: str = Form(...), model: str = Form(...), year: int = Form(...),
    db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageBusFleet"))
):
    try:
        crud.create_bus(db, make, model, year)
        return RedirectResponse(url=f"/buses?message=Bus created successfully!", status_code=303)

    except Exception as e:
        return RedirectResponse(url=f"/buses?error={str(e)}", status_code=303)
    

@fleet_router.get("/maintenance", response_class=HTMLResponse)
async def get_maintenance(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageBusFleet"))):
    try:
        maintenance = crud.get_maintenance(db)
        return templates.TemplateResponse("maintenance.html", {"request": request, "maintenance": maintenance})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@fleet_router.get("/maintenance/new", response_class=HTMLResponse)
async def create_maintenance(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageBusFleet"))):
    try:
        buses = crud.get_buses(db)
        
        return templates.TemplateResponse("add_maintenance.html", {"request": request, "buses": buses})
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching bus details: {str(e)}")



@fleet_router.post("/maintenance/new")
async def create_bus(
    id: str = Form(...), date: str = Form(...),
    db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageBusFleet"))
):
    try:
        crud.create_maintenance(db, id, date)
        return RedirectResponse(url=f"/maintenance?message=Maintenance created successfully!", status_code=303)

    except Exception as e:
        return RedirectResponse(url=f"/maintenance?error={str(e)}", status_code=303)