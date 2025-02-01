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
        user = crud.get_user_by_username(db, current_user["username"])
        user_id = user["id"]
        
        # Fetch roles of the current user
        roles = crud.get_user_roles(db, user_id)
        role_names = [role['name'] for role in roles]
        return templates.TemplateResponse("buses.html", {"request": request, "buses": buses, "current_user": user, "role_names": role_names})
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
    user = crud.get_user_by_username(db, current_user["username"])
    user_id = user["id"]
    
    # Fetch roles of the current user
    roles = crud.get_user_roles(db, user_id)
    role_names = [role['name'] for role in roles]
    return templates.TemplateResponse("add_bus.html", {"request": request, "current_user": user, "role_names": role_names})

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
        maintenances = crud.get_maintenance(db)
        user = crud.get_user_by_username(db, current_user["username"])
        user_id = user["id"]
        
        # Fetch roles of the current user
        roles = crud.get_user_roles(db, user_id)
        role_names = [role['name'] for role in roles]
        return templates.TemplateResponse("maintenance.html", {"request": request, "maintenances": maintenances, "current_user": user, "role_names": role_names})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@fleet_router.get("/maintenance/new", response_class=HTMLResponse)
async def create_maintenance(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageBusFleet"))):
    try:
        buses = crud.get_buses(db)
        user = crud.get_user_by_username(db, current_user["username"])
        user_id = user["id"]
        
        # Fetch roles of the current user
        roles = crud.get_user_roles(db, user_id)
        role_names = [role['name'] for role in roles]
        return templates.TemplateResponse("add_maintenance.html", {"request": request, "buses": buses, "current_user": user, "role_names": role_names})
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching buses details: {str(e)}")



@fleet_router.post("/maintenance/new")
async def create_maintenance(
    bus_id: str = Form(...), date: str = Form(...),
    db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageBusFleet"))
):
    try:
        crud.create_maintenance(db, bus_id, date)
        return RedirectResponse(url=f"/maintenance?message=Maintenance created successfully!", status_code=303)

    except Exception as e:
        return RedirectResponse(url=f"/maintenance?error={str(e)}", status_code=303)
    

@fleet_router.get("/maintenance/{maintenance_id}/edit", response_class=HTMLResponse)
async def edit_maintenance(
    maintenance_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_permission("ManageBusFleet"))
):
    try:
        maintenance = crud.get_maintenance_by_id(db, maintenance_id)
        if not maintenance:
            raise HTTPException(status_code=404, detail="Maintenance not found")
        
        buses = crud.get_buses(db)

        if not buses:
            raise HTTPException(status_code=404, detail="Buses not found")
        
        return templates.TemplateResponse(
            "edit_maintenance.html", {"request": request, "maintenance": maintenance, "buses": buses}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@fleet_router.post("/maintenance/{maintenance_id}/edit")
async def update_maintenance(
    maintenance_id: int,
    bus_id: str = Form(...),
    date: str = Form(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_permission("ManageBusFleet"))
):
    try:
        updated_maintenance = crud.update_maintenance(db, maintenance_id, bus_id, date)
        if not updated_maintenance:
            raise HTTPException(status_code=404, detail="Maintenance not found")
        return RedirectResponse(
            url=f"/maintenance?message=Maintenance updated successfully!", status_code=303
        )
    except Exception as e:
        return RedirectResponse(
            url=f"/maintenance?error={str(e)}", status_code=303
        )
