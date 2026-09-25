import logging
from sqlalchemy.orm import Session
from entity.programs import Programs
from exceptions import PruebaCreationError, PruebaNotFoundError


def listar(db: Session) -> list[Programs]:
    try:
        return db.query(Programs).order_by(Programs.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list programs: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_por_id(id_programa: int, db: Session) -> Programs | None:
    try:
        return db.query(Programs).filter(Programs.id == id_programa).first()
    except Exception as e:
        logging.error(f"Failed to get program by id: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_por_nombre(nombre: str, db: Session) -> Programs | None:
    try:
        return db.query(Programs).filter(Programs.name.ilike(nombre.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get program by name: {str(e)}")
        raise PruebaNotFoundError(str(e))


def crear(programa: Programs, db: Session) -> Programs:
    try:
        db.add(programa)
        db.commit()
        db.refresh(programa)
        return programa
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create program: {str(e)}")
        raise PruebaCreationError(str(e))


def actualizar(programa: Programs, db: Session) -> Programs:
    try:
        db.commit()
        db.refresh(programa)
        return programa
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to update program: {str(e)}")
        raise PruebaCreationError(str(e))
