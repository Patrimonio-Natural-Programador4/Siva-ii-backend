from sqlalchemy.orm import Session
from entity.agreements_products import AgreementsProducts
from entity.disbursement import Disbursement
from entity.disbursement_products import DisbursementProducts

def obtener_por_id_agreement(id_agreement: int, db: Session):
    return db.query(AgreementsProducts).filter(AgreementsProducts.id_agreement == id_agreement).all()


def obtener_desembolsos_por_id_agreement(id_agreement: int, db: Session):
    return db.query(Disbursement, AgreementsProducts).join(
        DisbursementProducts, DisbursementProducts.disbursement_id == Disbursement.id
    ).join(
        AgreementsProducts, AgreementsProducts.id == DisbursementProducts.product_id
    ).filter(
        AgreementsProducts.id_agreement == id_agreement
    ).order_by(
        Disbursement.number_disbursement.asc().nullslast(),
        Disbursement.id.asc(),
        AgreementsProducts.id.asc(),
    ).all()
