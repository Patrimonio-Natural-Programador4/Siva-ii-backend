import logging
from sqlalchemy.orm import Session
from entity.approval_categories import ApprovalCategory
from exceptions import PruebaNotFoundError

def obtener_por_codigo(code: str, db: Session) -> ApprovalCategory | None:
    try:
        return db.query(ApprovalCategory).filter(ApprovalCategory.code == code).first()
    except Exception as e:
        logging.error(f"Failed to get rol by id: {str(e)}")
        raise PruebaNotFoundError(str(e))