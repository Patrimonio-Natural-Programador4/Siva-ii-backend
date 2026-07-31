from typing import Optional

from pydantic import BaseModel

from dto.ViajesDTO import ViajesCreate

# acciones solicitud aprobacion


class AccionSolicitudAprobacion(BaseModel):
    id_adquisicion: Optional[str] = None
    id_solicitud_aprobacion: Optional[int] = None
    comentarios: Optional[str] = None
    tipo_accion: Optional[str] = None
    viaje: Optional[ViajesCreate] = None
    tipo_solicitud: Optional[str] = None  
    id_usuario_ajuste: Optional[int] = None
    usuario_solicito: Optional[bool] = None
    id_rol_aprobacion_ajuste: Optional[int] = None
    orden_actual: Optional[int] = None
    id_usuarios_mencion: Optional[list] = None
    class Config:
        from_attributes = True