from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Define templates for rendering HTML
templates = Jinja2Templates(directory="templates")

home_router = APIRouter()

@home_router.get("/", response_class=HTMLResponse)
def home(request: Request):
    username = request.session.get("username")  # Retrieve username from session
    return templates.TemplateResponse(
        "index.html", {"request": request, "username": username}
    )