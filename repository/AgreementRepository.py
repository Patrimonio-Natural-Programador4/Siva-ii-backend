import logging
from sqlalchemy.orm import Session,joinedload
from entity.agreements import Agreements
from dto.agreementDTO import AgreementsBase,AgreementsCreateBase
from sqlalchemy.exc import SQLAlchemyError
from exceptions import PruebaNotFoundError


def listar(db: Session):
    return (
        db.query(Agreements).order_by(Agreements.code.asc()).all() )  


from sqlalchemy.orm import Session, joinedload

def obtener_por_id(id: int, db: Session) -> Agreements | None:
    try:
        return (
            db.query(Agreements)
              .options(joinedload(Agreements.agreement_origin))
              .filter(Agreements.id == id)
              .first()
        )
    except Exception as e:
        logging.error(f"Error al obtener acuerdo por id: {str(e)}")
        raise PruebaNotFoundError(str(e))
    
    
    
def obtener_por_code(code: str, db: Session) -> Agreements | None:
    try:
        return (
            db.query(Agreements)
              .options(joinedload(Agreements.agreement_origin))
              .filter(Agreements.code== code)
              .first()
        )
    except Exception as e:
        logging.error(f"Error al obtener acuerdo por id: {str(e)}")
        raise PruebaNotFoundError(str(e))
    
def crear_agreement(agreement: Agreements, db: Session) -> Agreements:
    try:
        db.add(agreement)
        db.commit()
        db.refresh(agreement)
        return agreement
    except Exception as e:
        db.rollback()
        logging.error(f"Error al crear acuerdo: {str(e)}")
        raise