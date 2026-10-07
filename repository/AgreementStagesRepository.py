import logging
from sqlalchemy.orm import Session
from entity.agreement_stages import AgreementStages
from exceptions import PruebaNotFoundError



def listar(db: Session) -> list[AgreementStages]:
    try:
        return db.query(AgreementStages).order_by(AgreementStages.name.asc()).all()
    except Exception as e:
        logging.error(f"Error al listar fases de acuerdo: {str(e)}")
        raise PruebaNotFoundError(str(e))
    
    
def obtener_pad_por_id(id: int, db: Session) -> AgreementStages | None:
    try:
        return db.query(AgreementStages).filter(AgreementStages.id == id).first()
    except Exception as e:
        logging.error(f"Error al obtener fases de acuerdo por id: {str(e)}")
        raise PruebaNotFoundError(str(e))