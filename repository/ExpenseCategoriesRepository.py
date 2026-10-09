import logging
from sqlalchemy.orm import Session
from entity.expense_categories import ExpenseCategories
from exceptions import PruebaCreationError, PruebaNotFoundError

def list_expense_categories(db: Session) -> list[ExpenseCategories]:
    try:
        return db.query(ExpenseCategories).order_by(ExpenseCategories.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list ExpenseCategories: {str(e)}")
        raise PruebaNotFoundError(str(e))


def create_expense_categories(ExpenseCategories: ExpenseCategories, db: Session) -> ExpenseCategories:
    try:
        db.add(ExpenseCategories)
        db.commit()
        db.refresh(ExpenseCategories)
        return ExpenseCategories
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create ExpenseCategories: {str(e)}")
        raise PruebaCreationError(str(e))


def get_by_name_expense_categories(nombre: str, db: Session) -> ExpenseCategories | None:
    try:
        return db.query(ExpenseCategories).filter(ExpenseCategories.name.ilike(nombre.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get ExpenseCategories by name: {str(e)}")
        raise PruebaNotFoundError(str(e))