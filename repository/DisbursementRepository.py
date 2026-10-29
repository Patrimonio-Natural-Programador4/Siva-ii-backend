import logging
from sqlalchemy.orm import Session
from entity.disbursement import Disbursement
from exceptions import PruebaCreationError, PruebaNotFoundError


def list_disbursement(db: Session) -> list[Disbursement]:
    try:
        return db.query(Disbursement).order_by(Disbursement.id.desc()).all()
    except Exception as e:
        logging.error(f"Failed to list disbursement: {str(e)}")
        raise PruebaNotFoundError(str(e))


def get_disbursement_by_id(id: int, db: Session) -> Disbursement | None:
    try:
        return db.query(Disbursement).filter(Disbursement.id == id).first()
    except Exception as e:
        logging.error(f"Failed to get disbursement by id: {str(e)}")
        raise PruebaNotFoundError(str(e))


def get_disbursement_by_agreement(agreement_id: int, db: Session) -> list[Disbursement]:
    try:
        return (
            db.query(Disbursement)
            .filter(Disbursement.agreement_id == agreement_id)
            .order_by(Disbursement.number_disbursement.asc())
            .all()
        )
    except Exception as e:
        logging.error(f"Failed to get disbursement by agreement: {str(e)}")
        raise PruebaNotFoundError(str(e))


def get_disbursement_by_previous_studies(previous_studies_id: int, db: Session) -> list[Disbursement]:
    try:
        return (
            db.query(Disbursement)
            .filter(Disbursement.previous_studies_id == previous_studies_id)
            .order_by(Disbursement.number_disbursement.asc())
            .all()
        )
    except Exception as e:
        logging.error(f"Failed to get disbursement by previous studies: {str(e)}")
        raise PruebaNotFoundError(str(e))


def create_disbursement(disbursement: Disbursement, db: Session) -> Disbursement:
    try:
        db.add(disbursement)
        db.commit()
        db.refresh(disbursement)
        return disbursement
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create disbursement: {str(e)}")
        raise PruebaCreationError(str(e))


def update_disbursement(disbursement: Disbursement, db: Session) -> Disbursement:
    try:
        db.commit()
        db.refresh(disbursement)
        return disbursement
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to update disbursement: {str(e)}")
        raise PruebaCreationError(str(e))