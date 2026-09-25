import logging
from sqlalchemy.orm import Session
from entity.regions import Regions
from exceptions import PruebaCreationError, PruebaNotFoundError

def listar_departamentos(db: Session) -> list[Regions]:
    try:
        return db.query(Regions).filter(Regions.region_id == 6).order_by(Regions.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list regions: {str(e)}")
        raise PruebaNotFoundError(str(e))
    
def listar_municipios(db: Session) -> list[Regions]:
    try:
        return db.query(Regions).filter(Regions.region_id != 6, Regions.region_id != None).order_by(Regions.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list regions: {str(e)}")
        raise PruebaNotFoundError(str(e))