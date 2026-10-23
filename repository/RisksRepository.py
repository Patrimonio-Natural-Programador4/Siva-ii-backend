import logging
from sqlalchemy.orm import Session
from entity.risks import Risks
from exceptions import PruebaCreationError, PruebaNotFoundError


def list_risks(db: Session) -> list[Risks]:
    try:
        return db.query(Risks).order_by(Risks.risk.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list risk: {str(e)}")
        raise PruebaNotFoundError(str(e))


def get_risk_by_id(id_risk: int, db: Session) -> Risks | None:
    try:
        return db.query(Risks).filter(Risks.id == id_risk).first()
    except Exception as e:
        logging.error(f"Failed to get risk by id: {str(e)}")
        raise PruebaNotFoundError(str(e))


def get_risk_by_risk(risk: str, db: Session) -> Risks | None:
    try:
        return db.query(Risks).filter(Risks.risk.ilike(risk.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get risk by name: {str(e)}")
        raise PruebaNotFoundError(str(e))


def create_risk(risk: Risks, db: Session) -> Risks:
    try:
        db.add(risk)
        db.commit()
        db.refresh(risk)
        return risk
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create risk: {str(e)}")
        raise PruebaCreationError(str(e))


def update_risk(risk: Risks, db: Session) -> Risks:
    try:
        db.commit()
        db.refresh(risk)
        return risk
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to update risk: {str(e)}")
        raise PruebaCreationError(str(e))
