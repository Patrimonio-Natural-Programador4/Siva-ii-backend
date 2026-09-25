from typing import Optional
from pydantic import BaseModel, Field


class AccesoModulosBase(BaseModel):
    id_acceso_modulo: Optional[int] = None
    id_rol: Optional[int] = None
    id_modulo: Optional[int] = None
    acceso_modulo: Optional[bool] = None
    descripcion: Optional[str] = None
    modulo: Optional[str] = None


class AccesoControlesBase(BaseModel):
    id_acceso_control: Optional[int] = None
    id_rol: Optional[int] = None
    id_control: Optional[int] = None
    acceso_control: Optional[bool] = None


class RolesBase(BaseModel):
    id_rol: Optional[int] = None
    rol: Optional[str] = None
    descripcion: Optional[str] = None
    acceso_modulos: list[AccesoModulosBase] = Field(default_factory=list)
    acceso_controles: list[AccesoControlesBase] = Field(default_factory=list)

    class Config:
        from_attributes = True


class RolesCreateBase(BaseModel):
    rol: Optional[str] = None
    descripcion: Optional[str] = None
    acceso_modulos: list[AccesoModulosBase] = Field(default_factory=list)
    acceso_controles: list[AccesoControlesBase] = Field(default_factory=list)
