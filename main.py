from fastapi import FastAPI

from source.api.routers import dishes, menus, submenus

app = FastAPI()

app.include_router(menus.router)
app.include_router(submenus.router)
app.include_router(dishes.router)
