
from typing import Optional
from pydantic import BaseModel
from dto.RolesArpobacionUsuariosDTO import RolesAprobacionUsuariosBase  # Assuming this import is correct
from dto.FlujosAprobacionRutaDTO import FlujosAprobacionRutaBase  # Assuming this import is correct

class MenuBase(BaseModel):
    id_menu: Optional[int] = None
    nombre_menu: Optional[str] = None
    id_menu_padre: Optional[int] = None
    orden_menu: Optional[int] = None
    id_modulo: Optional[int] = None
    icono: Optional[str] = None
    url: Optional[str] = None
    valor_padre: Optional[str] = None
    orden_padre: Optional[int] = None
    id_rol: Optional[int] = None
    icono_padre: Optional[str] = None
    url_padre: Optional[str] = None
    class Config:
        from_attributes = True