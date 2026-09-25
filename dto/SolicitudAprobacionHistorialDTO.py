from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel
from datetime import date

class SolicitudAprobacionHistorialDTOBase(BaseModel):
    id_historial: Optional[int] = None
    id_solicitud_aprobacion: Optional[int] = None
    id_registro_asociado: Optional[int] = None
    id_flujo_aprobacion: Optional[int] = None
    id_categoria: Optional[int] = None
    id_estado_aprobacion_solicitud: Optional[int] = None
    id_rol_aprobacion: Optional[int] = None
    id_usuario: Optional[int] = None
    id_estado_aprobacion_ruta: Optional[int] = None
    fecha_aprobacion: Optional[datetime] = None
    fecha_crea: Optional[datetime] = None
    observaciones: Optional[str] = None
    id_ruta: Optional[int] = None
    orden: Optional[int] = None
    asigna_presupuesto_viajes: Optional[bool] = None
    ajusta_itinerario_viajes: Optional[bool] = None
    rol: Optional[str] = None
    usuario: Optional[str] = None
    categoria_aprobacion: Optional[str] = None
    guid:  Optional[uuid.UUID] = None
    estado_aprobacion_ruta: Optional[str] = None
    deshabilita_conceptos_anticipo: Optional[bool] = None
    valida_soportes_hotel: Optional[bool] = None
    agrega_rpc: Optional[bool] = None
    agrega_documento_contable: Optional[bool] = None

    class Config:
        from_attributes = True