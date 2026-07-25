import logging
from sqlalchemy.orm import Session
from entity.approval_requests import ApprovalRequests
from exceptions import PruebaNotFoundError

def numero_solicitudes(db: Session) -> int:
    try:
        solicitudes = db.query(ApprovalRequests).count()
        return solicitudes
    except Exception as e:
        logging.error(f"Failed to fetch solicitudes de aprobación: {str(e)}")
        raise PruebaNotFoundError(str(e))