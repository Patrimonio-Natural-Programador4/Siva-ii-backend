import logging
from sqlalchemy.orm import Session
from entity.document_types import DocumentTypes
from exceptions import PruebaCreationError, PruebaNotFoundError


def listar(db: Session) -> list[DocumentTypes]:
    try:
        return db.query(DocumentTypes).order_by(DocumentTypes.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list DocumentTypes: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_por_id(id: int, db: Session) -> DocumentTypes | None:
    try:
        return db.query(DocumentTypes).filter(DocumentTypes.id == id).first()
    except Exception as e:
        logging.error(f"Failed to get dosuments_types by id: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_por_nombre(nombre: str, db: Session) -> DocumentTypes | None:
    try:
        return db.query(DocumentTypes).filter(DocumentTypes.name.ilike(nombre.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get documents types by name: {str(e)}")
        raise PruebaNotFoundError(str(e))


def crear(doctu: DocumentTypes, db: Session) -> DocumentTypes:
    try:
        db.add(doctu)
        db.commit()
        db.refresh(doctu)
        return doctu
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create documents types: {str(e)}")
        raise PruebaCreationError(str(e))


def actualizar(doctu: DocumentTypes, db: Session) -> DocumentTypes:
    try:
        db.commit()
        db.refresh(doctu)
        return doctu
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to documents types program: {str(e)}")
        raise PruebaCreationError(str(e))
