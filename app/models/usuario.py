from pydantic import BaseModel

class Usuario(BaseModel):
    nombre: str
    apellido_paterno: str
    apellido_materno: str