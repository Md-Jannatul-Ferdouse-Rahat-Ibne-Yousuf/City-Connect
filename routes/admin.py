from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import crud
from database import get_db
from utils import *

# Define templates for rendering HTML
templates = Jinja2Templates(directory="templates")

admin_router = APIRouter()


# Page to create a new role
@admin_router.get("/create-role")
def create_role(
    request: Request,
    current_user: dict = Depends(require_permission("FullAccess"))
):
    return templates.TemplateResponse("create_role.html", {"request": request})
    

@admin_router.post("/create-role")
def create_role(
    name: str = Form(...), 
    description: str = Form(...), 
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_permission("FullAccess"))
):
    try:
        crud.create_role(db, name, description)
        return {"message": f"Role '{name}' created successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



# Page to create a new permission
@admin_router.get("/create-permission", response_class=HTMLResponse)
def create_permission_form(
    request: Request,
    current_user: dict = Depends(require_permission("FullAccess"))
    ):
    return templates.TemplateResponse("create_permission.html", {"request": request})


@admin_router.post("/create-permission")
def create_permission(
    name: str = Form(...), 
    description: str = Form(...), 
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_permission("FullAccess"))
    ):
    try:
        crud.create_permission(db, name, description)
        return {"message": f"Permission '{name}' created successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Page to assign a permission to a role
@admin_router.get("/assign-permission", response_class=HTMLResponse)
def assign_permission_form(
    request: Request, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_permission("FullAccess"))
    ):
    roles = crud.get_roles(db)
    permissions = crud.get_permissions(db)
    return templates.TemplateResponse("assign_permission.html", {"request": request, "roles": roles, "permissions": permissions})


@admin_router.post("/assign-permission")
def assign_permission(
    role_id: int = Form(...), 
    permission_id: int = Form(...), 
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_permission("FullAccess"))
    ):
    try:
        crud.assign_permission_to_role(db, role_id, permission_id)
        return {"message": "Permission assigned to role successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

