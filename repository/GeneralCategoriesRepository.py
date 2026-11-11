import logging
from sqlalchemy.orm import Session
from entity.general_categories import GeneralCategories
from exceptions import PruebaCreationError, PruebaNotFoundError

def list_general_categories(db: Session) -> list[GeneralCategories]:
    try:
        return db.query(GeneralCategories).order_by(GeneralCategories.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list general categories: {str(e)}")
        raise PruebaNotFoundError(str(e))


def create_general_categories(GeneralCategories: GeneralCategories, db: Session) -> GeneralCategories:
    try:
        db.add(GeneralCategories)
        db.commit()
        db.refresh(GeneralCategories)
        return GeneralCategories
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create general categories: {str(e)}")
        raise PruebaCreationError(str(e))


def get_by_name_general_categories(nombre: str, db: Session) -> GeneralCategories | None:
    try:
        return db.query(GeneralCategories).filter(GeneralCategories.name.ilike(nombre.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get general categories by name: {str(e)}")
        raise PruebaNotFoundError(str(e))