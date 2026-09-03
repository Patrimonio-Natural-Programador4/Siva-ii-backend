from sqlalchemy.orm import Session
from dto.TravelLegalizationsDto import TravelLegalizationCreate, TravelLegalizationUpdate
from repository import TravelLegalizationsRepository
from decimal import Decimal

def crear_legalizacion(db: Session, legalizacion: TravelLegalizationCreate):
    return TravelLegalizationsRepository.crear_legalizacion(db, legalizacion)

def obtener_legalizaciones_por_viaje(db: Session, travel_request_id: int):
    return TravelLegalizationsRepository.obtener_legalizaciones_por_viaje(db, travel_request_id)

def obtener_legalizacion_por_viaje(db: Session, travel_request_id: int):
    return TravelLegalizationsRepository.obtener_legalizacion_por_viaje(db, travel_request_id)

def actualizar_legalizacion(db: Session, legalization_id: int, legalizacion: TravelLegalizationUpdate):
    existente = TravelLegalizationsRepository.obtener_legalizacion_por_id(db, legalization_id)
    if not existente:
        raise ValueError("No se encontró la legalización especificada.")

    datos_actualizar = legalizacion.dict(exclude_unset=True)

    subtotal = datos_actualizar.get('subtotal', existente.subtotal)
    iva = datos_actualizar.get('iva', existente.iva)
    retention_porcentage = datos_actualizar.get('retention_porcentage', existente.retention_porcentage)

    if 'retention' not in datos_actualizar and ('subtotal' in datos_actualizar or 'retention_porcentage' in datos_actualizar):
        datos_actualizar['retention'] = (Decimal(subtotal) * Decimal(retention_porcentage)) / Decimal(100)

    retention = datos_actualizar.get('retention', existente.retention)

    if 'amount_paid' not in datos_actualizar and ('subtotal' in datos_actualizar or 'iva' in datos_actualizar or 'retention' in datos_actualizar):
        datos_actualizar['amount_paid'] = Decimal(subtotal) + Decimal(iva) - Decimal(retention)

    return TravelLegalizationsRepository.actualizar_legalizacion(db, legalization_id, datos_actualizar)