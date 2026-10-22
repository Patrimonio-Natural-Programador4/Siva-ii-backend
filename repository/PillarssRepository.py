import logging
from sqlalchemy.orm import Session
from entity.pillars import Pillars
from exceptions import PruebaCreationError, PruebaNotFoundError

def listar(db: Session) -> list[Pillars]:
    try:
        #print ('Listar repo')
        return db.query(Pillars).order_by(Pillars.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list Pillars: {str(e)}")
        raise PruebaNotFoundError(str(e))

