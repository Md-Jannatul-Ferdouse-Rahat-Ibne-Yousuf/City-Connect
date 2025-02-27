from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
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
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_permission("FullAccess"))
):
    user = crud.get_user_by_username(db, current_user["username"])
    user_id = user["id"]
    
    # Fetch roles of the current user
    roles = crud.get_user_roles(db, user_id)
    role_names = [role['name'] for role in roles]
    return templates.TemplateResponse("create_role.html", {"request": request, "current_user": user, "role_names": role_names})
    

@admin_router.post("/create-role")
def create_role(
    name: str = Form(...), 
    description: str = Form(...), 
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_permission("FullAccess"))
):
    try:
        crud.create_role(db, name, description)
        return RedirectResponse(url=f"/dashboard?message=Role created successfully!", status_code=303)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



# Page to create a new permission
@admin_router.get("/create-permission", response_class=HTMLResponse)
def create_permission_form(
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_permission("FullAccess"))
    ):
    user = crud.get_user_by_username(db, current_user["username"])
    user_id = user["id"]
    
    # Fetch roles of the current user
    user_roles = crud.get_user_roles(db, user_id)
    role_names = [role['name'] for role in user_roles]
    return templates.TemplateResponse("create_permission.html", {"request": request, "current_user": user, "role_names": role_names})


@admin_router.post("/create-permission")
def create_permission(
    name: str = Form(...), 
    description: str = Form(...), 
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_permission("FullAccess"))
    ):
    try:
        crud.create_permission(db, name, description)
        return RedirectResponse(url=f"/dashboard?message=Permission created successfully!", status_code=303)
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

    user = crud.get_user_by_username(db, current_user["username"])
    user_id = user["id"]
    
    # Fetch roles of the current user
    user_roles = crud.get_user_roles(db, user_id)
    role_names = [role['name'] for role in user_roles]
    return templates.TemplateResponse("assign_permission.html", {"request": request, 
                                                                 "roles": roles, 
                                                                 "permissions": permissions, 
                                                                 "current_user": user, 
                                                                 "role_names": role_names})


@admin_router.post("/assign-permission")
def assign_permission(
    role_id: int = Form(...), 
    permission_id: int = Form(...), 
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_permission("FullAccess"))
    ):
    try:
        crud.assign_permission_to_role(db, role_id, permission_id)
        return RedirectResponse(url=f"/dashboard?message=Permission assigned successfully!", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

