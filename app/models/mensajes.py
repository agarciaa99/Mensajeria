from pydantic import BaseModel

class MensajeBase(BaseModel):
    id_emisor: int
    id_receptor: int
    contenido: str