import logging
from sqlalchemy.orm import Session
from entity.modalities import Modalities
from exceptions import PruebaCreationError, PruebaNotFoundError

def listar(db: Session) -> list[Modalities]:
    try:
        print ('Listar repo')
        return db.query(Modalities).order_by(Modalities.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list modalities: {str(e)}")
        raise PruebaNotFoundError(str(e))


def crear(modalities: Modalities, db: Session) -> Modalities:
    try:
        db.add(modalities)
        db.commit()
        db.refresh(modalities)
        return modalities
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create program: {str(e)}")
        raise PruebaCreationError(str(e))


def obtener_por_nombre(nombre: str, db: Session) -> Modalities | None:
    try:
        return db.query(Modalities).filter(Modalities.name.ilike(nombre.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get program by name: {str(e)}")
        raise PruebaNotFoundError(str(e))