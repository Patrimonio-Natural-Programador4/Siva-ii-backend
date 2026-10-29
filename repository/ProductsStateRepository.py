import logging
from sqlalchemy.orm import Session
from entity.products_state import ProductsState
from exceptions import PruebaCreationError, PruebaNotFoundError


def list_products_state(db: Session) -> list[ProductsState]:
    try:
        return db.query(ProductsState).order_by(ProductsState.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list ProductsState: {str(e)}")
        raise PruebaNotFoundError(str(e))


def get_products_state_by_id(id: int, db: Session) -> ProductsState | None:
    try:
        return db.query(ProductsState).filter(ProductsState.id == id).first()
    except Exception as e:
        logging.error(f"Failed to get  products state by id: {str(e)}")
        raise PruebaNotFoundError(str(e))


def get_products_state_by_state(state: str, db: Session) -> ProductsState | None:
    try:
        return db.query(ProductsState).filter(ProductsState.name.ilike(state.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get  products state by state: {str(e)}")
        raise PruebaNotFoundError(str(e))


def create_products_state(state: ProductsState, db: Session) -> ProductsState:
    try:
        db.add(state)
        db.commit()
        db.refresh(state)
        return state
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create products states: {str(e)}")
        raise PruebaCreationError(str(e))


def update_products_state(state: ProductsState, db: Session) -> ProductsState:
    try:
        db.commit()
        db.refresh(state)
        return state
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to update products states: {str(e)}")
        raise PruebaCreationError(str(e))
