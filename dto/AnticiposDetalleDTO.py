from datetime import datetime
import decimal
from typing import Optional
import uuid
from pydantic import BaseModel

class AnticiposDetalleBase(BaseModel):
    id_anticipo_detalle: Optional[int] = None
    id_anticipo: Optional[int] = None
    id_concepto: Optional[int] = None
    valor_anticipo: Optional[decimal.Decimal] = None
    valor_legalizado: Optional[decimal.Decimal] = None
    id_proyecto: Optional[int] = None
    id_rubro: Optional[int] = None
    rubro: Optional[str] = None
    observaciones: Optional[str] = None
    concepto: Optional[str] = None
    editado: Optional[bool] = None
    proyecto: Optional[str] = None
    notificacion_supervisores: Optional[str] = None
    ids_notificacion_supervisores: Optional[list] = None
    modificado: Optional[bool] = None
    requiere_ajuste: Optional[bool] = None
    deshabilitado: Optional[bool] = None
    es_legalizacion: Optional[bool] = None
    class Config:
        from_attributes = True