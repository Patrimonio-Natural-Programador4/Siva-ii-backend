import logging
from sqlalchemy.orm import Session
from entity.previous_studies_states import PreviousStudiesStates
from exceptions import PruebaCreationError, PruebaNotFoundError


def listar_estudios_previos_estado(db: Session) -> list[PreviousStudiesStates]:
    try:
        return db.query(PreviousStudiesStates).order_by(PreviousStudiesStates.state.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list PreviousStudiesStates: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_estudios_previos_estado_por_id(id: int, db: Session) -> PreviousStudiesStates | None:
    try:
        return db.query(PreviousStudiesStates).filter(PreviousStudiesStates.id == id).first()
    except Exception as e:
        logging.error(f"Failed to get previous studies states by id: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_estudios_previos_estado_por_estado(state: str, db: Session) -> PreviousStudiesStates | None:
    try:
        return db.query(PreviousStudiesStates).filter(PreviousStudiesStates.state.ilike(state.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get previous studies states by state: {str(e)}")
        raise PruebaNotFoundError(str(e))


def crear_estudios_previos_estado(estudio: PreviousStudiesStates, db: Session) -> PreviousStudiesStates:
    try:
        db.add(estudio)
        db.commit()
        db.refresh(estudio)
        return estudio
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create previous studies states: {str(e)}")
        raise PruebaCreationError(str(e))


def actualizar_estudios_previos_estado(estudio: PreviousStudiesStates, db: Session) -> PreviousStudiesStates:
    try:
        db.commit()
        db.refresh(estudio)
        return estudio
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to update previous studies states: {str(e)}")
        raise PruebaCreationError(str(e))
