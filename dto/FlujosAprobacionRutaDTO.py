
from typing import Optional
from pydantic import BaseModel
from dto.RolesArpobacionUsuariosDTO import RolesAprobacionUsuariosBase  # Assuming this import is correct

class FlujosAprobacionRutaBase(BaseModel):
    id_ruta: Optional[int] = None
    id_flujo_aprobacion: Optional[int] = None
    id_rol_aprobacion: Optional[int] = None
    orden: Optional[int] = None
    activo: Optional[bool] = None
    rol: Optional[str] = None
    descripcion: Optional[str] = None
    label_aprobacion: Optional[str] = None
    label_ajuste: Optional[str] = None
    asigna_revisor: Optional[bool] = None
    label_pendiente: Optional[str] = None

    class Config:
        from_attributes = True