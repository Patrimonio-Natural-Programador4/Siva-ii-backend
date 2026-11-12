import logging
from sqlalchemy import exists
from sqlalchemy.orm import Session, aliased
from entity.activities import Activities
from exceptions import PruebaCreationError, PruebaNotFoundError

def Activities_list(db: Session) -> list[Activities]:
    try:
        daughter = aliased(Activities)
        return ( 
                db.query(Activities).filter(~exists().where(daughter.activity_id==Activities.id))
                .order_by(Activities.code.asc()).all()
                )
    except Exception as e:
        logging.error(f"Failed to list Activities: {str(e)}")
        raise PruebaNotFoundError(str(e))




"""
def create_activity(Activities: Activities, db: Session) -> Activities:
    try:
        db.add(Activities)
        db.commit()
        db.refresh(Activities)
        return Activities
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create activity: {str(e)}")
        raise PruebaCreationError(str(e))


def obtener_por_nombre(nombre: str, db: Session) -> Activities | None:
    try:
        return db.query(Activities).filter(Activities.name.ilike(nombre.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get program by name: {str(e)}")
        raise PruebaNotFoundError(str(e))
"""