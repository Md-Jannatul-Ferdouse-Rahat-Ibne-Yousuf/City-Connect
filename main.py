from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles

import uvicorn

# Import routers
from routes.admin import admin_router
from routes.auth import auth_router
from routes.home import home_router
from routes.dashboard import dashboard_router
from routes.register import register_router
from routes.driver import driver_router
from routes.hr import hr_router
from routes.fleet_manager import fleet_router
from routes.station_manager import station_router
from routes.routes_manager import route_router
from routes.logout_route import logout_router

from initialize import *

# First time initialization
# run_initializers()

app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="secret-key")

app.mount("/static", StaticFiles(directory="static"), name="static")


# Include routers
app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(home_router)
app.include_router(dashboard_router)
app.include_router(register_router)
app.include_router(hr_router)
app.include_router(fleet_router)
app.include_router(station_router)
app.include_router(route_router)
app.include_router(logout_router)
app.include_router(driver_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
