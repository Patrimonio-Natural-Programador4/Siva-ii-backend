import logging
from sqlalchemy.orm import Session
from entity.pads import Pads
from exceptions import PruebaCreationError, PruebaNotFoundError


def listar(db: Session) -> list[Pads]:
    try:
        return db.query(Pads).order_by(Pads.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list Pads: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_pad_por_id(id: int, db: Session) -> Pads | None:
    try:
        return db.query(Pads).filter(Pads.id == id).first()
    except Exception as e:
        logging.error(f"Failed to get Pads by id: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_pad_por_nombre(name: str, db: Session) -> Pads | None:
    try:
        return db.query(Pads).filter(Pads.name.ilike(name.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get Pads by name: {str(e)}")
        raise PruebaNotFoundError(str(e))


def crear_pad(pad: Pads, db: Session) -> Pads:
    try:
        db.add(pad)
        db.commit()
        db.refresh(pad)
        return pad
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create pads: {str(e)}")
        raise PruebaCreationError(str(e))


def actualizar_pad(pad: Pads, db: Session) -> Pads:
    try:
        db.commit()
        db.refresh(pad)
        return pad
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to update pads: {str(e)}")
        raise PruebaCreationError(str(e))
