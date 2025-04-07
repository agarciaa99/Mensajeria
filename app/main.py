from fastapi import FastAPI
from app.routers import usuarios
from app.routers import mensajes
from app.routers import login

app = FastAPI()

app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(mensajes.router, prefix="/mensajes", tags=["Mensajes"])
app.include_router(login.router, tags=["Login"])