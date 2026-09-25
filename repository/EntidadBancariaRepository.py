import logging
from sqlalchemy.orm import Session
from entity.banks import Banks
from exceptions import PruebaNotFoundError

def listar(db: Session) -> list[Banks]:
    try:
        tipos_cuenta = db.query(Banks).all()
        return tipos_cuenta
    except Exception as e:
        logging.error(f"Failed to fetch entidades bancarias: {str(e)}")
        raise PruebaNotFoundError(str(e))