from typing import Optional

from pydantic import BaseModel, Field


class RolesAprobacionUsuariosBase(BaseModel):
    id_rol_usuario: Optional[int] = None
    id_rol_aprobacion: Optional[int] = None
    id_usuario: Optional[int] = None
    activo: Optional[bool] = None
    usuario: Optional[str] = None
    area: Optional[str] = None
    correo: Optional[str] = None


class RolesAprobacionBase(BaseModel):
    id_rol_aprobacion: Optional[int] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None
    usuarios: list[RolesAprobacionUsuariosBase] = Field(default_factory=list)


class FlujosAprobacionRutaBase(BaseModel):
    id_ruta: Optional[int] = None
    id_flujo_aprobacion: Optional[int] = None
    id_rol_aprobacion: Optional[int] = None
    orden: Optional[int] = None
    activo: Optional[bool] = None
    rol: Optional[str] = None
    descripcion: Optional[str] = None


class FlujosAprobacionBase(BaseModel):
    id_flujo_aprobacion: Optional[int] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None
    categoria: Optional[str] = None
    rutas: list[FlujosAprobacionRutaBase] = Field(default_factory=list)
    id_categoria: Optional[int] = None


class UsuarioDelegadoBase(BaseModel):
    id_usuario: Optional[int] = None
    nombre: Optional[str] = None


class DelegacionRolesUsuariosBase(BaseModel):
    id_delegacion_roles_usuarios: Optional[int] = None
    id_usuario: Optional[int] = None
    id_rol_aprobacion: Optional[int] = None
    ids_usuarios_delegados: list[int] = Field(default_factory=list)
    usuario: Optional[str] = None
    rol_aprobacion: Optional[str] = None
    usuarios_delegados: list[UsuarioDelegadoBase] = Field(default_factory=list)