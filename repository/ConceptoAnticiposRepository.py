import logging
from sqlalchemy.orm import Session
from entity.expense_advance_concepts import ExpenseAdvanceConcepts
from exceptions import PruebaNotFoundError

def listar(db: Session) -> list[ExpenseAdvanceConcepts]:
    try:
        tipos_cuenta = db.query(ExpenseAdvanceConcepts).order_by(ExpenseAdvanceConcepts.concept).all()
        return tipos_cuenta
    except Exception as e:
        logging.error(f"Failed to fetch conceptos anticipos: {str(e)}")
        raise PruebaNotFoundError(str(e))