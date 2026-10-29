import logging
from sqlalchemy import text
from sqlalchemy.orm import Session
from entity.agreements_products import AgreementsProducts
from entity.disbursement import Disbursement
from entity.disbursement_products import DisbursementProducts
from exceptions import PruebaCreationError, PruebaNotFoundError

def list_agreements_products(db: Session) -> list[AgreementsProducts]:
    try:
        return db.query(AgreementsProducts).order_by(AgreementsProducts.id.desc()).all()
    except Exception as e:
        logging.error(f"Failed to list agreements_products: {str(e)}")
        raise PruebaNotFoundError(str(e))


def get_agreements_products_by_id(id: int, db: Session) -> AgreementsProducts | None:
    try:
        return db.query(AgreementsProducts).filter(AgreementsProducts.id == id).first()
    except Exception as e:
        logging.error(f"Failed to get agreements_products by id: {str(e)}")
        raise PruebaNotFoundError(str(e))


def get_agreements_products_by_agreement(agreement_id: int, db: Session) -> list[AgreementsProducts]:
    try:
        return (
            db.query(AgreementsProducts)
            .filter(AgreementsProducts.id_agreement == agreement_id)
            .order_by(AgreementsProducts.id.asc())
            .all()
        )
    except Exception as e:
        logging.error(f"Failed to get agreements products by agreement: {str(e)}")
        raise PruebaNotFoundError(str(e))


def get_agreements_products_by_previous_studies(previous_studies_id: int, db: Session) -> list[AgreementsProducts]:
    try:
        return (
            db.query(AgreementsProducts)
            .filter(AgreementsProducts.previous_studies_id == previous_studies_id)
            .order_by(AgreementsProducts.id.asc())
            .all()
        )
    except Exception as e:
        logging.error(f"Failed to get agreements_products by previous studies: {str(e)}")
        raise PruebaNotFoundError(str(e))


def create_agreements_products(agreements_products: AgreementsProducts, db: Session) -> AgreementsProducts:
    try:
        db.add(agreements_products)
        db.commit()
        db.refresh(agreements_products)
        return agreements_products
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create agreements products: {str(e)}")
        raise PruebaCreationError(str(e))


def update_agreements_products(agreements_products: AgreementsProducts, db: Session) -> AgreementsProducts:
    try:
        db.commit()
        db.refresh(agreements_products)
        return agreements_products
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to update agreements products: {str(e)}")
        raise PruebaCreationError(str(e))


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



def get_tree_by_previous_studies(previous_studies_id: int, db: Session):
    try:
        result = db.execute(
            text("SELECT fn_arbol_productos_estudio_previo(:id)"),
            {"id": previous_studies_id}
        ).scalar()
        return result or []
    except Exception as e:
        logging.error(f"Failed to get products tree by previous studies: {str(e)}")
        raise PruebaNotFoundError(str(e))