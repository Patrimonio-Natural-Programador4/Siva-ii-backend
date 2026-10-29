import logging
from sqlalchemy.orm import Session
from entity.disbursement_state import DisbursementState
from exceptions import PruebaCreationError, PruebaNotFoundError


def list_disbursement_state(db: Session) -> list[DisbursementState]:
    try:
        return db.query(DisbursementState).order_by(DisbursementState.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list DisbursementState: {str(e)}")
        raise PruebaNotFoundError(str(e))


def get_disbursement_state_by_id(id: int, db: Session) -> DisbursementState | None:
    try:
        return db.query(DisbursementState).filter(DisbursementState.id == id).first()
    except Exception as e:
        logging.error(f"Failed to get  disbursement state by id: {str(e)}")
        raise PruebaNotFoundError(str(e))


def get_disbursement_state_by_state(state: str, db: Session) -> DisbursementState | None:
    try:
        return db.query(DisbursementState).filter(DisbursementState.name.ilike(state.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get  disbursement state by state: {str(e)}")
        raise PruebaNotFoundError(str(e))


def create_disbursement_state(state: DisbursementState, db: Session) -> DisbursementState:
    try:
        db.add(state)
        db.commit()
        db.refresh(state)
        return state
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create disbursement states: {str(e)}")
        raise PruebaCreationError(str(e))


def update_disbursement_state(state: DisbursementState, db: Session) -> DisbursementState:
    try:
        db.commit()
        db.refresh(state)
        return state
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to update disbursement states: {str(e)}")
        raise PruebaCreationError(str(e))
