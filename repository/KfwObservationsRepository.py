import logging
from sqlalchemy.orm import Session
from entity.kfw_observations import KfwObservations
from exceptions import PruebaCreationError, PruebaNotFoundError

def list_kfw_observations(db: Session) -> list[KfwObservations]:
    try:
        return db.query(KfwObservations).order_by(KfwObservations.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list Kfw Observations: {str(e)}")
        raise PruebaNotFoundError(str(e))


def create_kfw_observations(KfwObservations: KfwObservations, db: Session) -> KfwObservations:
    try:
        db.add(KfwObservations)
        db.commit()
        db.refresh(KfwObservations)
        return KfwObservations
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create Kfw Observations: {str(e)}")
        raise PruebaCreationError(str(e))


def get_by_name_kfw_observations(nombre: str, db: Session) -> KfwObservations | None:
    try:
        return db.query(KfwObservations).filter(KfwObservations.name.ilike(nombre.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get Kfw Observations by name: {str(e)}")
        raise PruebaNotFoundError(str(e))