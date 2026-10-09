import logging
from sqlalchemy.orm import Session
from entity.purchase_types import PurchaseTypes
from exceptions import PruebaCreationError, PruebaNotFoundError

def list_purchase_types(db: Session) -> list[PurchaseTypes]:
    try:
        return db.query(PurchaseTypes).order_by(PurchaseTypes.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list PurchaseTypes: {str(e)}")
        raise PruebaNotFoundError(str(e))


def create_purchase_types(PurchaseTypes: PurchaseTypes, db: Session) -> PurchaseTypes:
    try:
        db.add(PurchaseTypes)
        db.commit()
        db.refresh(PurchaseTypes)
        return PurchaseTypes
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create PurchaseTypes: {str(e)}")
        raise PruebaCreationError(str(e))


def get_by_name_purchase_types(nombre: str, db: Session) -> PurchaseTypes | None:
    try:
        return db.query(PurchaseTypes).filter(PurchaseTypes.name.ilike(nombre.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get PurchaseTypes by name: {str(e)}")
        raise PruebaNotFoundError(str(e))