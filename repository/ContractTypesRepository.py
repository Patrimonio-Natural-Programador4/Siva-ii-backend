import logging
from sqlalchemy.orm import Session
from entity.contract_types import ContractTypes
from exceptions import PruebaCreationError, PruebaNotFoundError

def list_contract_types(db: Session) -> list[ContractTypes]:
    try:
        return db.query(ContractTypes).order_by(ContractTypes.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list ContractTypes: {str(e)}")
        raise PruebaNotFoundError(str(e))


def create_contract_types(ContractTypes: ContractTypes, db: Session) -> ContractTypes:
    try:
        db.add(ContractTypes)
        db.commit()
        db.refresh(ContractTypes)
        return ContractTypes
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create ContractTypes: {str(e)}")
        raise PruebaCreationError(str(e))


def get_by_name_contract_types(nombre: str, db: Session) -> ContractTypes | None:
    try:
        return db.query(ContractTypes).filter(ContractTypes.name.ilike(nombre.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get ContractTypes by name: {str(e)}")
        raise PruebaNotFoundError(str(e))