import logging
from sqlalchemy.orm import Session
from entity.agreement_origins import AgreementOrigins
from exceptions import PruebaCreationError, PruebaNotFoundError

def list_agreement_origins(db: Session) -> list[AgreementOrigins]:
    try:
        return db.query(AgreementOrigins).order_by(AgreementOrigins.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list AgreementOrigins: {str(e)}")
        raise PruebaNotFoundError(str(e))


def create_agreement_origins(AgreementOrigins: AgreementOrigins, db: Session) -> AgreementOrigins:
    try:
        db.add(AgreementOrigins)
        db.commit()
        db.refresh(AgreementOrigins)
        return AgreementOrigins
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create AgreementOrigins: {str(e)}")
        raise PruebaCreationError(str(e))


def get_by_name_agreement_origins(nombre: str, db: Session) -> AgreementOrigins | None:
    try:
        return db.query(AgreementOrigins).filter(AgreementOrigins.name.ilike(nombre.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get AgreementOrigins by name: {str(e)}")
        raise PruebaNotFoundError(str(e))