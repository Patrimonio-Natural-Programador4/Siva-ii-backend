import logging
from sqlalchemy.orm import Session, selectinload
from entity.roles import Roles
from entity.permissions import Permissions
from entity.modules import Modules
from entity.controls import Controls
from entity.module_access import ModuleAccess
from entity.control_access import ControlAccess
from exceptions import PruebaNotFoundError


def listar(db: Session) -> list[Roles]:
    try:
        return db.query(Roles).options(selectinload(Roles.permission)).order_by(Roles.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list roles: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_por_id(id_rol: int, db: Session) -> Roles | None:
    try:
        return db.query(Roles).options(selectinload(Roles.permission)).filter(Roles.id == id_rol).first()
    except Exception as e:
        logging.error(f"Failed to get rol by id: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_por_nombre(nombre: str, db: Session) -> Roles | None:
    try:
        return db.query(Roles).filter(Roles.name.ilike(nombre.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get rol by nombre: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_guard_name_default(db: Session) -> str:
    try:
        rol = db.query(Roles).order_by(Roles.id.asc()).first()
        if rol and rol.guard_name:
            return rol.guard_name
        return 'web'
    except Exception:
        return 'web'


def listar_permisos(db: Session) -> list[Permissions]:
    try:
        return db.query(Permissions).order_by(Permissions.category.asc(), Permissions.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list permissions: {str(e)}")
        raise PruebaNotFoundError(str(e))


def listar_modulos_activos(db: Session) -> list[Modules]:
    try:
        return (
            db.query(Modules)
            .filter(Modules.is_active.is_(True))
            .order_by(Modules.order.asc(), Modules.name.asc())
            .all()
        )
    except Exception as e:
        logging.error(f"Failed to list active modules: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_modulos_por_ids(ids_modulos: list[int], db: Session) -> list[Modules]:
    try:
        if not ids_modulos:
            return []

        return (
            db.query(Modules)
            .filter(Modules.id.in_(ids_modulos), Modules.is_active.is_(True))
            .order_by(Modules.order.asc(), Modules.name.asc())
            .all()
        )
    except Exception as e:
        logging.error(f"Failed to get modules by ids: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_permisos_por_nombres(nombres: list[str], db: Session) -> list[Permissions]:
    try:
        if not nombres:
            return []

        return db.query(Permissions).filter(Permissions.name.in_(nombres)).all()
    except Exception as e:
        logging.error(f"Failed to get permissions by names: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_permisos_por_ids(ids_permisos: list[int], db: Session) -> list[Permissions]:
    try:
        if not ids_permisos:
            return []
        return db.query(Permissions).filter(Permissions.id.in_(ids_permisos)).all()
    except Exception as e:
        logging.error(f"Failed to get permissions by ids: {str(e)}")
        raise PruebaNotFoundError(str(e))


def crear(rol: Roles, db: Session) -> Roles:
    try:
        db.add(rol)
        db.flush()
        db.refresh(rol)
        return rol
    except Exception as e:
        logging.error(f"Failed to create rol: {str(e)}")
        raise PruebaNotFoundError(str(e))


def guardar(db: Session):
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to commit transaction: {str(e)}")
        raise PruebaNotFoundError(str(e))


# ── Controles ────────────────────────────────────────────────────────────────

def listar_controles_por_modulo(ids_modulos: list[int], db: Session) -> list[Controls]:
    try:
        if not ids_modulos:
            return []
        return db.query(Controls).filter(Controls.module_id.in_(ids_modulos)).order_by(Controls.code.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list controls: {str(e)}")
        raise PruebaNotFoundError(str(e))


# ── AccesoModulos ─────────────────────────────────────────────────────────────

def listar_acceso_modulos_rol(id_rol: int, db: Session) -> list[ModuleAccess]:
    try:
        return db.query(ModuleAccess).filter(ModuleAccess.role_id == id_rol).all()
    except Exception as e:
        logging.error(f"Failed to list module access: {str(e)}")
        raise PruebaNotFoundError(str(e))


# ── AccesoControles ───────────────────────────────────────────────────────────

def listar_acceso_controles_rol(id_rol: int, db: Session) -> list[ControlAccess]:
    try:
        return db.query(ControlAccess).filter(ControlAccess.role_id == id_rol).all()
    except Exception as e:
        logging.error(f"Failed to list control access: {str(e)}")
        raise PruebaNotFoundError(str(e))
