from sqlalchemy.orm import Session, joinedload
from entity.travel_legalizations import TravelLegalization
from dto.TravelLegalizationsDto import TravelLegalizationCreate
import logging

logger = logging.getLogger(__name__)

def crear_legalizacion(db: Session, legalizacion: TravelLegalizationCreate) -> TravelLegalization:
    try:
        nuevo_registro = TravelLegalization(**legalizacion.dict())
        db.add(nuevo_registro)
        db.commit()
        db.refresh(nuevo_registro)
        return nuevo_registro
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear legalizacion: {str(e)}")
        raise e

def obtener_legalizaciones_por_viaje(db: Session, travel_request_id: int) -> list[TravelLegalization]:
    return (
        db.query(TravelLegalization)
        .options(joinedload(TravelLegalization.regimen_type))
        .filter(TravelLegalization.travel_request_id == travel_request_id)
        .order_by(TravelLegalization.legalization_id.asc())
        .all()
    )

def obtener_legalizacion_por_viaje(db: Session, travel_request_id: int) -> TravelLegalization:
    return (
        db.query(TravelLegalization)
        .options(joinedload(TravelLegalization.regimen_type))
        .filter(TravelLegalization.travel_request_id == travel_request_id)
        .first()
    )

def obtener_legalizacion_por_id(db: Session, legalization_id: int) -> TravelLegalization:
    return (
        db.query(TravelLegalization)
        .options(joinedload(TravelLegalization.regimen_type))
        .filter(TravelLegalization.legalization_id == legalization_id)
        .first()
    )

def actualizar_legalizacion(db: Session, legalization_id: int, datos_actualizar: dict) -> TravelLegalization:
    try:
        legalizacion = (
            db.query(TravelLegalization)
            .options(joinedload(TravelLegalization.regimen_type))
            .filter(TravelLegalization.legalization_id == legalization_id)
            .first()
        )
        if not legalizacion:
            return None

        for key, value in datos_actualizar.items():
            if hasattr(legalizacion, key) and key != 'legalization_id':
                setattr(legalizacion, key, value)

        db.commit()
        db.refresh(legalizacion)
        db.expire(legalizacion, ['regimen_type'])
        return legalizacion
    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar legalizacion: {str(e)}")
        raise e
