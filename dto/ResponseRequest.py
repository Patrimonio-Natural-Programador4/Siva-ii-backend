from pydantic import BaseModel
from typing import Optional

class ResponseRequest(BaseModel):
    mensaje: Optional[str] = None
    identity: Optional[int] = None
    solicitud_exitosa: bool = False
    guid: Optional[str] = None
    ids_usuarios_notificar: Optional[list[int]] = []
    archivo: Optional[str] = None