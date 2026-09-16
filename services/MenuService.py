from pytest import Session
from sqlalchemy.orm import Session
from dto.MenuDTO import MenuBase
from repository import UsuariosRepository
from repository import MenuRepository
from exceptions import PruebaNotFoundError
import logging

def listar_menu_x_rol(usuario_guid: str, db: Session)-> list[MenuBase]:
    try:
        menuListDto = []
        usuario = UsuariosRepository.obtener_por_guid_msft(usuario_guid.strip(), db)
        ids_rol = [rol.role_id for rol in usuario.roles]
        if not ids_rol:
            return menuListDto
        menus = MenuRepository.listar_menu_x_rol(ids_rol, db)

        for menu in menus:
            menuListDto.append(MenuBase(
                id_menu=menu.menu_id,
                nombre_menu=menu.name,
                id_menu_padre=menu.parent_menu_id,
                orden_menu=menu.order_menu,
                id_modulo=menu.module_id,
                icono=menu.icon,
                url=menu.url,
                valor_padre=menu.parent_value,
                orden_padre=menu.parent_order,
                id_rol=menu.role_id,
                icono_padre=menu.parent_icon,
                url_padre=menu.parent_url
            ))

        return menuListDto
    except Exception as e:
        logging.error(f"Failed to list menu for user {usuario_guid}: {str(e)}")
        raise PruebaNotFoundError(str(e))
