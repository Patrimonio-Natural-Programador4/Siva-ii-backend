import logging
from sqlalchemy.orm import Session
from entity.agreement_types import AgreementTypes
from exceptions import PruebaCreationError, PruebaNotFoundError

def list_agreement_types(db: Session) -> list[AgreementTypes]:
    try:
        return db.query(AgreementTypes).order_by(AgreementTypes.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list AgreementTypes: {str(e)}")
        raise PruebaNotFoundError(str(e))


def create_agreement_types(AgreementTypes: AgreementTypes, db: Session) -> AgreementTypes:
    try:
        db.add(AgreementTypes)
        db.commit()
        db.refresh(AgreementTypes)
        return AgreementTypes
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create AgreementTypes: {str(e)}")
        raise PruebaCreationError(str(e))


def get_by_name_agreement_types(nombre: str, db: Session) -> AgreementTypes | None:
    try:
        return db.query(AgreementTypes).filter(AgreementTypes.name.ilike(nombre.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get AgreementTypes by name: {str(e)}")
        raise PruebaNotFoundError(str(e))