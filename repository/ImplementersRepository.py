import logging
from sqlalchemy.orm import Session
from entity.implementers import Implementers
from exceptions import PruebaCreationError, PruebaNotFoundError


def listar_implementadoras(db: Session) -> list[Implementers]:
    try:
        return db.query(Implementers).order_by(Implementers.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list Implementers: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_implemntadora_por_id(id: int, db: Session) -> Implementers | None:
    try:
        return db.query(Implementers).filter(Implementers.id == id).first()
    except Exception as e:
        logging.error(f"Failed to get Implementers by id: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_implemntadora_por_acronimo(acronymm: str, db: Session) -> Implementers | None:
    try:
        return db.query(Implementers).filter(Implementers.acronym.ilike(acronymm.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get Implementers by name: {str(e)}")
        raise PruebaNotFoundError(str(e))


def crear_implementadora(imp: Implementers, db: Session) -> Implementers:
    try:
        db.add(imp)
        db.commit()
        db.refresh(imp)
        return imp
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create Implementers: {str(e)}")
        raise PruebaCreationError(str(e))


def actualizar_implemntadora(imp: Implementers, db: Session) -> Implementers:
    try:
        db.commit()
        db.refresh(imp)
        return imp
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to update Implementers: {str(e)}")
        raise PruebaCreationError(str(e))
