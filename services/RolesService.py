import logging
from sqlalchemy.orm import Session

from dto.ListaGenerica import ListaGenerica
from dto.ListadosDTO import Listados
from dto.ResponseRequest import ResponseRequest
from dto.RolesDTO import AccesoControlesBase, AccesoModulosBase, RolesBase, RolesCreateBase
from entity.roles import Roles
from entity.acceso_modulos import AccesoModulos
from entity.acceso_controles import AccesoControles
from exceptions import PruebaCreationError, PruebaNotFoundError
from repository import RolesRepository


# == Listados ==================================================================

def listar_roles(db: Session) -> list[RolesBase]:
    roles = RolesRepository.listar(db)
    return [
        RolesBase(
            id_rol=int(rol.id),
            rol=rol.name,
            descripcion=rol.description,
            acceso_modulos=[],
            acceso_controles=[]
        )
        for rol in roles
    ]


def listar_modulos(db: Session) -> list[Listados]:
    modulos_db = RolesRepository.listar_modulos_activos(db)
    lista = [
        ListaGenerica(
            identity=int(m.id),
            valor=m.name,
            valor_referencia=m.description
        )
        for m in modulos_db
    ]
    return [Listados(id_listado=1, tipo_listado='MODULOS', lista_generica=lista)]


def listar_controles_por_modulo(ids_modulos: list[int], db: Session) -> list[Listados]:
    controles_db = RolesRepository.listar_controles_por_modulo(ids_modulos, db)
    lista = [
        ListaGenerica(
            identity=int(c.id_control),
            valor=c.codigo,
            idrelacion=int(c.id_modulo),
            valorNumerico=None,
            valor_referencia=None,
            checked=False
        )
        for c in controles_db
    ]
    return [Listados(id_listado=2, tipo_listado='CONTROLES', lista_generica=lista)]


# == Obtener por ID ============================================================

def obtener_rol_por_id(id_rol: int, db: Session) -> RolesBase | None:
    rol = RolesRepository.obtener_por_id(id_rol, db)
    if not rol:
        return None

    acceso_modulos_db = RolesRepository.listar_acceso_modulos_rol(id_rol, db)
    acceso_controles_db = RolesRepository.listar_acceso_controles_rol(id_rol, db)

    acceso_modulos = [
        AccesoModulosBase(
            id_acceso_modulo=int(am.id_acceso_modulo),
            id_rol=int(am.id_rol),
            id_modulo=int(am.id_modulo),
            acceso_modulo=am.acceso_modulo,
            modulo=am.modules.name if am.modules else None,
            descripcion=am.modules.description if am.modules else None
        )
        for am in acceso_modulos_db
    ]

    acceso_controles = [
        AccesoControlesBase(
            id_acceso_control=int(ac.id_acceso_control),
            id_rol=int(ac.id_rol),
            id_control=int(ac.id_control),
            acceso_control=ac.acceso_control
        )
        for ac in acceso_controles_db
    ]

    return RolesBase(
        id_rol=int(rol.id),
        rol=rol.name,
        descripcion=rol.description,
        acceso_modulos=acceso_modulos,
        acceso_controles=acceso_controles
    )


# == Crear =====================================================================

def crear_rol(payload: RolesCreateBase, db: Session) -> ResponseRequest:
    respuesta = ResponseRequest(solicitud_exitosa=False)

    nombre = (payload.rol or '').strip()
    if not nombre:
        respuesta.mensaje = 'El nombre del rol es obligatorio'
        return respuesta

    if RolesRepository.obtener_por_nombre(nombre, db):
        respuesta.mensaje = 'Ya existe un rol con ese nombre'
        return respuesta

    guard_name = RolesRepository.obtener_guard_name_default(db)
    rol = Roles(
        name=nombre,
        description=(payload.descripcion or '').strip() or None,
        guard_name=guard_name
    )

    try:
        RolesRepository.crear(rol, db)
        _actualizar_acceso_modulos(rol, payload.acceso_modulos, db)
        _actualizar_acceso_controles(rol, payload.acceso_controles, db)
        RolesRepository.guardar(db)

        respuesta.solicitud_exitosa = True
        respuesta.mensaje = 'Rol creado correctamente'
        respuesta.identity = int(rol.id)
        return respuesta
    except Exception as e:
        db.rollback()
        import logging
        logging.error(f"Failed to create rol: {str(e)}")
        return ResponseRequest(solicitud_exitosa=False, mensaje=str(e))


# == Actualizar ================================================================

def actualizar_rol(id_rol: int, payload: RolesCreateBase, db: Session) -> ResponseRequest:
    respuesta = ResponseRequest(solicitud_exitosa=False)

    rol = RolesRepository.obtener_por_id(id_rol, db)
    if not rol:
        respuesta.mensaje = 'Rol no encontrado'
        return respuesta

    nombre = (payload.rol or '').strip()
    if not nombre:
        respuesta.mensaje = 'El nombre del rol es obligatorio'
        return respuesta

    existente = RolesRepository.obtener_por_nombre(nombre, db)
    if existente and int(existente.id) != int(id_rol):
        respuesta.mensaje = 'Ya existe un rol con ese nombre'
        return respuesta

    try:
        rol.name = nombre
        rol.description = (payload.descripcion or '').strip() or None

        _actualizar_acceso_modulos(rol, payload.acceso_modulos, db)
        _actualizar_acceso_controles(rol, payload.acceso_controles, db)
        RolesRepository.guardar(db)

        respuesta.solicitud_exitosa = True
        respuesta.mensaje = 'Rol actualizado correctamente'
        respuesta.identity = int(rol.id)
        return respuesta
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to update rol: {str(e)}")
        return ResponseRequest(solicitud_exitosa=False, mensaje=str(e))


# == Helpers acceso ============================================================

def _actualizar_acceso_modulos(rol: Roles, acceso_modulos: list[AccesoModulosBase], db: Session) -> None:
    id_rol = int(rol.id)
    actuales = RolesRepository.listar_acceso_modulos_rol(id_rol, db)
    ids_actuales = {int(am.id_modulo) for am in actuales}
    ids_nuevos = {int(m.id_modulo) for m in acceso_modulos if m.id_modulo is not None}

    for id_modulo in (ids_actuales - ids_nuevos):
        db.query(AccesoModulos).filter(
            AccesoModulos.id_rol == id_rol,
            AccesoModulos.id_modulo == id_modulo
        ).delete()
        logging.info(f"AccesoModulo eliminado: rol={id_rol} modulo={id_modulo}")

    for m in acceso_modulos:
        if m.id_modulo is not None and int(m.id_modulo) not in ids_actuales:
            db.add(AccesoModulos(
                id_rol=id_rol,
                id_modulo=int(m.id_modulo),
                acceso_modulo=True
            ))
            logging.info(f"AccesoModulo insertado: rol={id_rol} modulo={m.id_modulo}")


def _actualizar_acceso_controles(rol: Roles, acceso_controles: list[AccesoControlesBase], db: Session) -> None:
    id_rol = int(rol.id)
    actuales = RolesRepository.listar_acceso_controles_rol(id_rol, db)
    ids_actuales = {int(ac.id_control) for ac in actuales}
    ids_nuevos = {int(c.id_control) for c in acceso_controles if c.id_control is not None}

    for id_control in (ids_actuales - ids_nuevos):
        db.query(AccesoControles).filter(
            AccesoControles.id_rol == id_rol,
            AccesoControles.id_control == id_control
        ).delete()
        logging.info(f"AccesoControl eliminado: rol={id_rol} control={id_control}")

    for c in acceso_controles:
        if c.id_control is not None and int(c.id_control) not in ids_actuales:
            db.add(AccesoControles(
                id_rol=id_rol,
                id_control=int(c.id_control),
                acceso_control=True
            ))
            logging.info(f"AccesoControl insertado: rol={id_rol} control={c.id_control}")
