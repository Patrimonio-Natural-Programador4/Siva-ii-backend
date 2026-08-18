import logging
from sqlalchemy.orm import Session
from entity.capacity_assessments import CapacityAssessments
from exceptions import PruebaCreationError, PruebaNotFoundError


def listar(db: Session) -> list[CapacityAssessments]:
    try:
        return db.query(CapacityAssessments).order_by(CapacityAssessments.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list CapacityAssessments: {str(e)}")
        raise PruebaNotFoundError(str(e))


def crear(capacidad: CapacityAssessments, db: Session) -> CapacityAssessments:
    try:
        db.add(capacidad)
        db.commit()
        db.refresh(capacidad)
        return capacidad
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create CapacityAssessments: {str(e)}")
        raise PruebaCreationError(str(e))


def obtener_por_id(id: int, db: Session) -> CapacityAssessments | None:
    try:
        return db.query(CapacityAssessments).filter(CapacityAssessments.id == id).first()
    except Exception as e:
        logging.error(f"Failed to get CapacityAssessments by id: {str(e)}")
        raise PruebaNotFoundError(str(e))
    
def obtener_por_nombre(nombre: str, db: Session) -> Modalities | None:
    try:
        return db.query(Modalities).filter(Modalities.name.ilike(nombre.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get program by name: {str(e)}")
        raise PruebaNotFoundError(str(e))