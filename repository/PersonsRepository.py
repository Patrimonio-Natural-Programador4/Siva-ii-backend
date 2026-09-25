import logging
from sqlalchemy.orm import Session
from entity.persons import Persons
from exceptions import PruebaCreationError, PruebaNotFoundError


def listar(db: Session) -> list[Persons]:
    try:
        return db.query(Persons).order_by(Persons.first_name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list Persons: {str(e)}")
        raise PruebaNotFoundError(str(e))


def crear(person: Persons, db: Session) -> Persons:
    try:
        db.add(person)
        db.commit()
        db.refresh(person)
        return person
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create Persons: {str(e)}")
        raise PruebaCreationError(str(e))
