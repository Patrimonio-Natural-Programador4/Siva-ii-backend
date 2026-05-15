
from typing import Optional
from pydantic import BaseModel
from dto.RolesArpobacionUsuariosDTO import RolesAprobacionUsuariosBase  # Assuming this import is correct
from dto.FlujosAprobacionRutaDTO import FlujosAprobacionRutaBase  # Assuming this import is correct

class FlujosAprobacionBase(BaseModel):
    id_flujo_aprobacion: Optional[int] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None
    categoria: Optional[str] = None  # Assuming RolesAprobacionUsuariosBase is defined elsewhere
    rutas: Optional[list[FlujosAprobacionRutaBase]] = None  # Assuming RolesAprobacionUsuariosBase is defined elsewhere
    id_categoria: Optional[int] = None  # Assuming this is an integer field representing the category ID
    class Config:
        from_attributes = True