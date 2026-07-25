from typing import Optional
from pydantic import BaseModel
from datetime import date

class ViajesItinerarioBase(BaseModel):
   
    id_viaje_itinerario: Optional[int] = None
    id_viaje: Optional[int] = None
    fecha: Optional[date] = None
    id_municipio_destino: Optional[int] = None
    id_municipio_origen: Optional[int] = None
    hora: Optional[str] = None
    observaciones: Optional[str] = None
    vereda_origen: Optional[str] = None
    destino_vereda: Optional[bool] = None
    origen_vereda: Optional[bool] = None
    vereda_destino: Optional[str] = None
    departamento_destino: Optional[str] = None
    municipio_destino: Optional[str] = None
    departamento_origen: Optional[str] = None
    municipio_origen: Optional[str] = None
    editado: Optional[bool] = None
    soporte_pase_abordar: Optional[str] = None
    soporte_tiquetes: Optional[str] = None
    es_zona_rural: Optional[bool] = None
    observaciones_zona_rural: Optional[str] = None
    id_departamento_origen: Optional[int] = None
    id_departamento_destino: Optional[int] = None
    ruta_soporte_tiquetes: Optional[str] = None
    ruta_soporte_pase_abordar: Optional[str] = None
    requiere_tiquetes_aereos: Optional[bool] = None
    id_proyecto: Optional[int] = None
    id_rubro: Optional[int] = None
    proyecto: Optional[str] = None
    rubro: Optional[str] = None

    class Config:
        from_attributes = True