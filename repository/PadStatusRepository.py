import logging
from sqlalchemy.orm import Session
from entity.padstatus import PadStatus
from exceptions import PruebaCreationError, PruebaNotFoundError

def list_pad_status(db: Session) -> list[PadStatus]:
    try:
        return db.query(PadStatus).order_by(PadStatus.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list PadStatus: {str(e)}")
        raise PruebaNotFoundError(str(e))


def create_pad_status(PadStatus: PadStatus, db: Session) -> PadStatus:
    try:
        db.add(PadStatus)
        db.commit()
        db.refresh(PadStatus)
        return PadStatus
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create PadStatus: {str(e)}")
        raise PruebaCreationError(str(e))


def get_by_name_pad_status(nombre: str, db: Session) -> PadStatus | None:
    try:
        return db.query(PadStatus).filter(PadStatus.name.ilike(nombre.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get PadStatus by name: {str(e)}")
        raise PruebaNotFoundError(str(e))