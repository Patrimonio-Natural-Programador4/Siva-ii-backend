from datetime import date
from typing import Optional
from pydantic import BaseModel

class ViajesHotelBase(BaseModel):
    id_viaje_hotel: Optional[int] = None
    id_viaje: Optional[int] = None
    id_municipio: Optional[int] = None
    observaciones: Optional[str] = None
    fecha_llegada: Optional[date] = None
    fecha_salida: Optional[date] = None
    departamento: Optional[str] = None
    municipio: Optional[str] = None
    tipo_alojamiento: Optional[str] = None  # Assuming this is a string field for type of accommodation
    editado: Optional[bool] = None
    soporte: Optional[str] = None
    ruta_soporte: Optional[str] = None
    pago_gestiona_fundacion: Optional[bool] = None  # New field added
    id_departamento: Optional[int] = None  # New field added
    id_proyecto: Optional[int] = None
    id_rubro: Optional[int] = None
    proyecto: Optional[str] = None
    rubro: Optional[str] = None
    class Config:
        from_attributes = True