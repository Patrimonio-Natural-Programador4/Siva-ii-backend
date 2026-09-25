import logging
from sqlalchemy.orm import Session

from entity.account_types import AccountTypes
from exceptions import PruebaNotFoundError

def listar(db: Session) -> list[AccountTypes]:
    try:
        tipos_cuenta = db.query(AccountTypes).all()
        return tipos_cuenta
    except Exception as e:
        logging.error(f"Failed to fetch tipos de cuenta: {str(e)}")
        raise PruebaNotFoundError(str(e))