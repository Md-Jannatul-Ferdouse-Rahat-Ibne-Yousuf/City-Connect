from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles

import uvicorn

# Import routers
from routes.auth import auth_router
from routes.home import home_router
from routes.dashboard import dashboard_router
from routes.register import register_router
from routes.driver import driver_router
from routes.hr import hr_router
from routes.fleet_manager import fleet_router
# from routes.role_management import role_router
# from routes.driver_management import driver_router
# from routes.timetable import timetable_router

from initialize import *

# First time initialization
# run_initializers()

app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="secret-key")

app.mount("/static", StaticFiles(directory="static"), name="static")


# Include routers
app.include_router(auth_router)
app.include_router(home_router)
app.include_router(dashboard_router)
app.include_router(register_router)
app.include_router(hr_router)
app.include_router(fleet_router)


# app.include_router(role_router)
# app.include_router(driver_router)
# app.include_router(timetable_router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
