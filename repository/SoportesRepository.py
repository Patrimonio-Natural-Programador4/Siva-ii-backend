import logging
from sqlalchemy.orm import Session
from entity.attachment_travel_tp import AttachmentTravelTp
from exceptions import PruebaNotFoundError, PruebaCreationError

logger = logging.getLogger(__name__)


def guardar_soporte(
    travel_request_id: int,
    nombre_archivo: str,
    ruta_archivo: str,
    db: Session
) -> AttachmentTravelTp:
    try:
        nuevo_registro = AttachmentTravelTp(
            attachment_name=nombre_archivo,
            path_document=str(ruta_archivo),
            travel_request_id=travel_request_id
        )
        db.add(nuevo_registro)
        db.commit()
        db.refresh(nuevo_registro)
        return nuevo_registro
    except Exception as e:
        db.rollback()
        logger.error(f"Error al guardar soporte en BD para viaje {travel_request_id}: {str(e)}")
        raise PruebaCreationError(str(e))


def guardar_o_reemplazar_soporte(
    travel_request_id: int,
    nombre_archivo: str,
    ruta_archivo: str,
    db: Session
) -> AttachmentTravelTp:
    """Alias compatible para guardar nuevo registro de soporte sin sobreescribir."""
    return guardar_soporte(travel_request_id, nombre_archivo, ruta_archivo, db)


def obtener_soporte_por_travel_request_id(
    travel_request_id: int,
    db: Session
) -> AttachmentTravelTp | None:
    try:
        return (
            db.query(AttachmentTravelTp)
            .filter(AttachmentTravelTp.travel_request_id == travel_request_id)
            .order_by(AttachmentTravelTp.id.desc())
            .first()
        )
    except Exception as e:
        logger.error(f"Error al obtener soporte para viaje {travel_request_id}: {str(e)}")
        raise PruebaNotFoundError(str(e))


def listar_soportes_por_travel_request_id(
    travel_request_id: int,
    db: Session
) -> list[AttachmentTravelTp]:
    try:
        return (
            db.query(AttachmentTravelTp)
            .filter(AttachmentTravelTp.travel_request_id == travel_request_id)
            .order_by(AttachmentTravelTp.id.asc())
            .all()
        )
    except Exception as e:
        logger.error(f"Error al listar soportes para viaje {travel_request_id}: {str(e)}")
        raise PruebaNotFoundError(str(e))
