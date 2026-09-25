
from typing import Optional
from pydantic import BaseModel

class RolesAprobacionUsuariosBase(BaseModel):
    id_rol_usuario: Optional[int] = None
    id_rol_aprobacion: Optional[int] = None
    id_usuario: Optional[int] = None
    activo: Optional[bool] = None
    usuario: Optional[str] = None  # Assuming usuario is a string field representing the user
    class Config:
        from_attributes = True