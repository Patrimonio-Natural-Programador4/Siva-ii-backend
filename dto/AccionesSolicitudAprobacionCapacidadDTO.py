from typing import Optional
from pydantic import BaseModel


class AccionSolicitudAprobacionCapacidad(BaseModel):
    id_solicitud_aprobacion: Optional[int] = None
    id_evaluacion: Optional[int] = None
    comentarios: Optional[str] = None
    tipo_accion: Optional[str] = None
    tipo_solicitud: Optional[str] = None
    id_usuario_ajuste: Optional[int] = None
    id_rol_aprobacion_ajuste: Optional[int] = None
    orden_actual: Optional[int] = None

    class Config:
        from_attributes = True