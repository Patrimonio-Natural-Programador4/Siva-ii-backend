import logging
from sqlalchemy.orm import Session
from entity.implementer_types import Implementer_types
from exceptions import PruebaCreationError, PruebaNotFoundError


def listar(db: Session) -> list[Implementer_types]:
    try:
        return db.query(Implementer_types).order_by(Implementer_types.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list Implementer_types: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_tipos_implementadora_por_id(id: int, db: Session) -> Implementer_types | None:
    try:
        return db.query(Implementer_types).filter(Implementer_types.id == id).first()
    except Exception as e:
        logging.error(f"Failed to get implementer_types by id: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_tipos_implementadora_por_name(name: str, db: Session) -> Implementer_types | None:
    try:
        return db.query(Implementer_types).filter(Implementer_types.name.ilike(name.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get implementer_types by name: {str(e)}")
        raise PruebaNotFoundError(str(e))


def crear_tipos_implementadora(implementer_types: Implementer_types, db: Session) -> Implementer_types:
    try:
        db.add(implementer_types)
        db.commit()
        db.refresh(implementer_types)
        return implementer_types
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create implementer_types: {str(e)}")
        raise PruebaCreationError(str(e))


def actualizar(implementer_types: Implementer_types, db: Session) -> Implementer_types:
    try:
        db.commit()
        db.refresh(implementer_types)
        return implementer_types
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to update implementer_types: {str(e)}")
        raise PruebaCreationError(str(e))
