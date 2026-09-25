
from typing import Optional
from pydantic import BaseModel
from dto.RolesArpobacionUsuariosDTO import RolesAprobacionUsuariosBase  # Assuming this import is correct

class RolesAprobacionBase(BaseModel):
    id_rol_aprobacion: Optional[int] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None
    usuarios: Optional[list[RolesAprobacionUsuariosBase]] = None  # Assuming RolesAprobacionUsuariosBase is defined elsewhere
    class Config:
        from_attributes = True