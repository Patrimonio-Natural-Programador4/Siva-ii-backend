import logging
from sqlalchemy.orm import Session
from entity.codes import Codes
from exceptions import PruebaCreationError, PruebaNotFoundError

def list_codes(db: Session) -> list[Codes]:
    try:
        return db.query(Codes).order_by(Codes.code.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list Codes: {str(e)}")
        raise PruebaNotFoundError(str(e))


def create_codes(Codes: Codes, db: Session) -> Codes:
    try:
        db.add(Codes)
        db.commit()
        db.refresh(Codes)
        return Codes
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create Codes: {str(e)}")
        raise PruebaCreationError(str(e))


def get_by_name_codes(code: str, db: Session) -> Codes | None:
    try:
        return db.query(Codes).filter(Codes.code.ilike(code.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get Codes by name: {str(e)}")
        raise PruebaNotFoundError(str(e))