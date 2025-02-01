from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import crud

def get_current_user(request: Request):
    current_user = {}
    current_user["username"] = request.session.get("username")
    current_user["role_names"] = request.session.get("role_names")
    current_user["permissions"] = request.session.get("permissions")

    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return current_user

def require_permission(permission: str):
    def _require_permission(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
        if not current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

        user_info = crud.get_user_by_username(db, current_user["username"])
        permissions = crud.get_user_permissions(db, user_info['id'])
        if permission not in permissions:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        
        return current_user

    return _require_permission