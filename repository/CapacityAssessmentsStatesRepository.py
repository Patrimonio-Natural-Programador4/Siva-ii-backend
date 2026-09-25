import logging
from sqlalchemy.orm import Session
from entity.capacity_assessments_states import CapacityAssessmentsStates
from exceptions import PruebaCreationError, PruebaNotFoundError


def listar(db: Session) -> list[CapacityAssessmentsStates]:
    try:
        return db.query(CapacityAssessmentsStates).order_by(CapacityAssessmentsStates.state.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list CapacityAssessmentsStates: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_capacity_assessments_states_por_id(id: int, db: Session) -> CapacityAssessmentsStates | None:
    try:
        return db.query(CapacityAssessmentsStates).filter(CapacityAssessmentsStates.id == id).first()
    except Exception as e:
        logging.error(f"Failed to get capacity assessments states by id: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_capacity_assessments_states_por_estado(state: str, db: Session) -> CapacityAssessmentsStates | None:
    try:
        return db.query(CapacityAssessmentsStates).filter(CapacityAssessmentsStates.state.ilike(state.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get capacity assessments states by state: {str(e)}")
        raise PruebaNotFoundError(str(e))


def crear_capacity_assessments_states(evaluacion: CapacityAssessmentsStates, db: Session) -> CapacityAssessmentsStates:
    try:
        db.add(evaluacion)
        db.commit()
        db.refresh(evaluacion)
        return evaluacion
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create capacity assessments states: {str(e)}")
        raise PruebaCreationError(str(e))


def actualizar_capacity_assessments_states(evaluacion: CapacityAssessmentsStates, db: Session) -> CapacityAssessmentsStates:
    try:
        db.commit()
        db.refresh(evaluacion)
        return evaluacion
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to update capacity assessments states: {str(e)}")
        raise PruebaCreationError(str(e))
