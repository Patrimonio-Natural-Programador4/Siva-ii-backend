import logging
from sqlalchemy.orm import Session
from entity.vw_menu import VwMenu
from exceptions import PruebaNotFoundError

def listar_menu_x_rol(ids_rol: list[int], db: Session) -> list[VwMenu]:
    try:
        menu = db.query(VwMenu).filter(VwMenu.role_id.in_(ids_rol)).distinct().all()
        return menu
    except Exception as e:
        logging.error(f"Failed to fetch menu items: {str(e)}")
        raise PruebaNotFoundError(str(e))