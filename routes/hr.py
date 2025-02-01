from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import crud
from database import get_db
from utils import *

# Define templates for rendering HTML
templates = Jinja2Templates(directory="templates")

hr_router = APIRouter()

# 1. Update Driver Salary
@hr_router.get("/driver-salary", response_class=HTMLResponse)
async def update_driver_salary_form(request: Request, current_user: dict = Depends(require_permission("EditDriverSalary"))):
    return templates.TemplateResponse("update_driver_salary.html", {"request": request})


@hr_router.post("/driver-salary")
async def update_driver_salary(
    driver_id: int = Form(...), salary: float = Form(...), 
    db: Session = Depends(get_db), current_user: dict = Depends(require_permission("EditDriverSalary"))
):
    try:
        crud.update_driver_salary(db, driver_id, salary)
        return {"message": "Driver salary updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 2. Add Driver
@hr_router.get("/add-driver", response_class=HTMLResponse)
async def add_driver_form(request: Request, current_user: dict = Depends(require_permission("ManageDrivers"))):
    return templates.TemplateResponse("add_driver.html", {"request": request})


@hr_router.post("/add-driver")
async def add_driver(
    name: str = Form(...), age: int = Form(...), license_no: str = Form(...),
    db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageDrivers"))
):
    try:
        crud.add_driver(db, name, age, license_no)
        return {"message": "Driver added successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 3. Update Driver Details
@hr_router.get("/update-driver/{driver_id}", response_class=HTMLResponse)
async def update_driver_form(request: Request, driver_id: int, current_user: dict = Depends(require_permission("ManageDrivers"))):
    return templates.TemplateResponse("update_driver.html", {"request": request, "driver_id": driver_id})


@hr_router.post("/update-driver/{driver_id}")
async def update_driver(
    driver_id: int, name: str = Form(None), age: int = Form(None),
    db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageDrivers"))
):
    try:
        print(f"Driver id: {driver_id}")
        crud.update_driver(db, driver_id, name, age)
        return {"message": "Driver details updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 4. Delete Driver
@hr_router.get("/delete-driver", response_class=HTMLResponse)
async def delete_driver_form(request: Request, current_user: dict = Depends(require_permission("ManageDrivers"))):
    return templates.TemplateResponse("delete_driver.html", {"request": request})


@hr_router.post("/delete-driver")
async def delete_driver(
    driver_id: int = Form(...), db: Session = Depends(get_db),
    current_user: dict = Depends(require_permission("ManageDrivers"))
):
    try:
        crud.delete_driver(db, driver_id)
        return {"message": "Driver deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 5. View Driver Timetable
@hr_router.get("/driver-timetable", response_class=HTMLResponse)
async def driver_timetable_form(request: Request, current_user: dict = Depends(require_permission("ViewTimetable"))):
    return templates.TemplateResponse("driver_timetable.html", {"request": request})


@hr_router.get("/driver-timetable-data")
async def driver_timetable(driver_id: int, db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ViewTimetable"))):
    try:
        timetable = crud.get_driver_timetable(db, driver_id)
        return {"timetable": timetable}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 6. Assign Drivers to Routes
@hr_router.get("/assign-route", response_class=HTMLResponse)
async def assign_route_form(request: Request, current_user: dict = Depends(require_permission("ManageRoutes"))):
    return templates.TemplateResponse("assign_route.html", {"request": request})


@hr_router.post("/assign-route")
async def assign_route(
    driver_id: int = Form(...), route_id: int = Form(...),
    db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageRoutes"))
):
    try:
        crud.assign_driver_to_route(db, driver_id, route_id)
        return {"message": "Driver assigned to route successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@hr_router.get("/drivers")
async def get_drivers(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageDrivers"))):
    try:
        drivers = crud.get_drivers(db)

        user = crud.get_user_by_username(db, current_user["username"])
        user_id = user["id"]
        
        roles = crud.get_user_roles(db, user_id)
        role_names = [role['name'] for role in roles]

        return templates.TemplateResponse("drivers.html", {"request": request, "drivers": drivers, "current_user": user, "role_names": role_names})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    

@hr_router.get("/driver-salaries/{driver_id}")
async def get_driver_salary(request: Request, driver_id: int, db: Session = Depends(get_db), current_user: dict = Depends(require_permission("ManageDrivers"))):
    try:
        driver_salary = crud.get_driver_salary(db, driver_id)
        if not driver_salary:
            driver_salary = [{
                "driver_id": driver_id,
                "id": id,
                "salary": 0.00,
                "year": "N/A",
                "month": "N/A",
                "hourly": 0.00,
                "hours_worked": 0,
            }]
        print(f"Driver: {driver_salary}")

        user = crud.get_user_by_username(db, current_user["username"])
        user_id = user["id"]
        
        # Fetch roles of the current user
        roles = crud.get_user_roles(db, user_id)
        role_names = [role['name'] for role in roles]

        return templates.TemplateResponse("driver_salaries.html", {"request": request, "driver_salary": driver_salary, "current_user": user, "role_names": role_names})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@hr_router.get("/drivers/edit/{driver_id}")
async def edit_driver(
    request: Request,
    driver_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_permission("ManageDrivers"))
):
    try:
        driver = crud.get_driver_by_id(db, driver_id)
        if not driver:
            raise HTTPException(status_code=404, detail="Driver not found.")

        user = crud.get_user_by_username(db, current_user["username"])
        user_id = user["id"]
        
        # Fetch roles of the current user
        roles = crud.get_user_roles(db, user_id)
        role_names = [role['name'] for role in roles]

        return templates.TemplateResponse("edit_driver.html", {"request": request, "driver": driver, "current_user": user, "role_names": role_names})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@hr_router.post("/drivers/edit/{driver_id}")
async def update_driver(
    driver_id: int,
    username: str = Form(...),
    email: str = Form(...),
    phone_number: str = Form(...),
    license_number: str = Form(...),
    experience_years: int = Form(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_permission("ManageDrivers"))
):
    try:
        updated_driver = crud.update_driver(
            db, driver_id, username, email, phone_number, license_number, experience_years
        )
        if not updated_driver:
            raise HTTPException(status_code=404, detail="Driver not found.")
        # Redirect with a success message
        return RedirectResponse(url=f"/drivers?message=Driver updated successfully!", status_code=303)
    except Exception as e:
        # Redirect with an error message
        return RedirectResponse(url=f"/drivers?error={str(e)}", status_code=303)


@hr_router.get("/add-salary/{driver_id}")
async def add_salary_page(request:Request, driver_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user = crud.get_user_by_username(db, current_user["username"])
    user_id = user["id"]
    
    # Fetch roles of the current user
    roles = crud.get_user_roles(db, user_id)
    role_names = [role['name'] for role in roles]
    return templates.TemplateResponse("add_salary.html", {"request": request, "driver_id": driver_id, "current_user": user, "role_names": role_names})


@hr_router.post("/add-salary/{driver_id}")
async def add_salary(
    driver_id: int,
    year: int = Form(...),
    month: str = Form(...),
    hourly: float = Form(...),
    hours_worked: int = Form(...),
    salary: float = Form(...),
    db: Session = Depends(get_db)
):
    try:
        print(f"Salary: {salary}")
        result = crud.add_salary(db, driver_id, year, month, hourly, hours_worked, salary)
        return RedirectResponse(url=f"/driver-salaries/{driver_id}", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@hr_router.get("/update-salary/{salary_id}")
async def show_update_salary(request: Request, salary_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        salary_record = crud.get_salary_record(db, salary_id)
        if not salary_record:
            raise HTTPException(status_code=404, detail="Salary record not found.")
        
        user = crud.get_user_by_username(db, current_user["username"])
        user_id = user["id"]
        
        # Fetch roles of the current user
        roles = crud.get_user_roles(db, user_id)
        role_names = [role['name'] for role in roles]
        return templates.TemplateResponse("update_salary.html", {"request": request, "salary_id": salary_id, 
                                                                 "salary_record": salary_record, 
                                                                 "current_user": user, "role_names": role_names})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@hr_router.post("/update-salary/{salary_id}")
async def update_salary(
    request: Request,
    salary_id: int,
    year: int = Form(...),
    month: str = Form(...),
    hourly: float = Form(...),
    hours_worked: int = Form(...),
    salary: float = Form(...),
    db: Session = Depends(get_db)
):
    try:
        driver_id = crud.update_salary(db, salary_id, year, month, hourly, hours_worked, salary)
        if not driver_id:
            raise HTTPException(status_code=404, detail="Salary record not found.")
        return RedirectResponse(url=f"/driver-salaries/{driver_id}", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))