from typing import Optional

from pydantic import BaseModel


class AccionesSolicitudAprobacionBase(BaseModel):
    id_solicitud_aprobacion: Optional[int] = None
    comentarios: Optional[str] = None
    tipo_accion: Optional[str] = None
    tipo_solicitud: Optional[str] = None
    id_usuario_ajuste: Optional[int] = None
    id_rol_aprobacion_ajuste: Optional[int] = None
    id_usuarios_mencion: Optional[list[int]] = None