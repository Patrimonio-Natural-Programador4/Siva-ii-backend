import logging
from sqlalchemy.orm import Session
from entity.Pidss import Pids
from exceptions import PruebaCreationError, PruebaNotFoundError

def listar(db: Session) -> list[Pids]:
    try:
        #print ('Listar repo')
        return db.query(Pids).order_by(Pids.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list Pids: {str(e)}")
        raise PruebaNotFoundError(str(e))

"""
def crear(Pids: Pids, db: Session) -> Pids:
    try:
        db.add(Pids)
        db.commit()
        db.refresh(Pids)
        return Pids
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create program: {str(e)}")
        raise PruebaCreationError(str(e))


def obtener_por_nombre(nombre: str, db: Session) -> Pids | None:
    try:
        return db.query(Pids).filter(Pids.name.ilike(nombre.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get program by name: {str(e)}")
        raise PruebaNotFoundError(str(e))
"""