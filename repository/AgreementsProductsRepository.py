from sqlalchemy.orm import Session
from entity.AgreementsProducts import AgreementsProducts

def obtener_por_id_agreement(id_agreement: int, db: Session):
    return db.query(AgreementsProducts).filter(AgreementsProducts.id_agreement == id_agreement).all()
