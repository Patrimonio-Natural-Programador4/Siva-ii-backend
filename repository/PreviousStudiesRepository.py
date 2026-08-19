#REPOSITORY ESTUDIOS PREVIOS

import logging
from sqlalchemy.orm import Session
from entity.previous_studies import PreviousStudies
from exceptions import PruebaCreationError, PruebaNotFoundError


def listar(db: Session) -> list[PreviousStudies]:
    try:
        return db.query(PreviousStudies).order_by(PreviousStudies.id.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list PreviousStudies: {str(e)}")
        raise PruebaNotFoundError(str(e))


def crear_estudio_previo(studies: PreviousStudies, db: Session) -> PreviousStudies:
    try:
        db.add(studies)
        db.commit()
        db.refresh(studies)
        return studies
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create PreviousStudies: {str(e)}")
        raise PruebaCreationError(str(e))


def obtener_por_id(id: int, db: Session) -> PreviousStudies | None:
    try:
        return db.query(PreviousStudies).filter(PreviousStudies.id == id).first()
    except Exception as e:
        logging.error(f"Failed to get PreviousStudies by id: {str(e)}")
        raise PruebaNotFoundError(str(e))
    
def obtener_por_nombre(nombre: str, db: Session) -> PreviousStudies | None:
    try:
        return db.query(PreviousStudies).filter(PreviousStudies.name.ilike(nombre.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get program by name: {str(e)}")
        raise PruebaNotFoundError(str(e))