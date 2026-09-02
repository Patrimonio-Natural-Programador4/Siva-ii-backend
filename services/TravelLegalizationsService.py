from sqlalchemy.orm import Session
from dto.TravelLegalizationsDto import TravelLegalizationCreate
from repository import TravelLegalizationsRepository

def crear_legalizacion(db: Session, legalizacion: TravelLegalizationCreate):
    existente = TravelLegalizationsRepository.obtener_legalizacion_por_viaje(db, legalizacion.travel_request_id)
    if existente:
        raise ValueError("El viaje ya tiene una legalización registrada.")
        
    return TravelLegalizationsRepository.crear_legalizacion(db, legalizacion)

def obtener_legalizacion_por_viaje(db: Session, travel_request_id: int):
    return TravelLegalizationsRepository.obtener_legalizacion_por_viaje(db, travel_request_id)
    