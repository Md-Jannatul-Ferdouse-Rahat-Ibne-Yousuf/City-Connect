from fastapi import APIRouter, Request, Depends, Form, HTTPException, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import crud
from database import get_db

# Define templates for rendering HTML
templates = Jinja2Templates(directory="templates")

logout_router = APIRouter()

@logout_router.get("/register", response_class=HTMLResponse)
async def logout(request: Request, response: Response):

    response.delete_cookie("username")
    return RedirectResponse(url="/", status_code=303)