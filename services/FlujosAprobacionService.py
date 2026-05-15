import logging
from typing import Optional

from sqlalchemy.orm import Session

from dto.FlujosAprobacionDTO import (
    DelegacionRolesUsuariosBase,
    FlujosAprobacionBase,
    FlujosAprobacionRutaBase,
    RolesAprobacionBase,
    RolesAprobacionUsuariosBase,
    UsuarioDelegadoBase,
)
from dto.ListaGenerica import ListaGenerica
from dto.ListadosDTO import Listados
from dto.ResponseRequest import ResponseRequest
from entity.categorias_aprobacion import CategoriasAprobacion
from entity.flujos_aprobacion import FlujosAprobacion
from entity.flujos_aprobacion_ruta import FlujosAprobacionRuta
from entity.roles_aprobacion import RolesAprobacion
from entity.roles_aprobacion_usuarios import RolesAprobacionUsuarios
from exceptions import PruebaCreationError, PruebaNotFoundError


def _full_name(user) -> str:
    return ' '.join(
        part.strip()
        for part in [user.first_name, user.other_name or '', user.last_name, user.other_last_name or '']
        if part and part.strip()
    )


# ---------------------------------------------------------------------------
# Roles de Aprobación
# ---------------------------------------------------------------------------

def listar_roles_aprobacion(db: Session) -> list[RolesAprobacionBase]:
    try:
        roles_db = db.query(RolesAprobacion).all()
        result = []
        for rol in roles_db:
            usuarios = []
            for u in rol.roles_usuarios:
                user = u.usuario
                usuarios.append(RolesAprobacionUsuariosBase(
                    id_rol_usuario=u.id_rol_usuario,
                    id_rol_aprobacion=u.id_rol_aprobacion,
                    id_usuario=u.id_usuario,
                    activo=u.activo,
                    usuario=_full_name(user) if user else None,
                    correo=user.email if user else None,
                    area=user.position if user else None,
                ))
            result.append(RolesAprobacionBase(
                id_rol_aprobacion=rol.id_rol_aprobacion,
                nombre=rol.nombre,
                descripcion=rol.descripcion,
                activo=rol.activo,
                usuarios=usuarios,
            ))
        return result
    except Exception as e:
        logging.error(f"Failed to list roles_aprobacion: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_rol_aprobacion_por_id(role_id: int, db: Session) -> Optional[RolesAprobacionBase]:
    try:
        rol = db.query(RolesAprobacion).filter(RolesAprobacion.id_rol_aprobacion == role_id).first()
        if not rol:
            return None
        usuarios = []
        for u in rol.roles_usuarios:
            user = u.usuario
            usuarios.append(RolesAprobacionUsuariosBase(
                id_rol_usuario=u.id_rol_usuario,
                id_rol_aprobacion=u.id_rol_aprobacion,
                id_usuario=u.id_usuario,
                activo=u.activo,
                usuario=_full_name(user) if user else None,
                correo=user.email if user else None,
                area=user.position if user else None,
            ))
        return RolesAprobacionBase(
            id_rol_aprobacion=rol.id_rol_aprobacion,
            nombre=rol.nombre,
            descripcion=rol.descripcion,
            activo=rol.activo,
            usuarios=usuarios,
        )
    except Exception as e:
        logging.error(f"Failed to get rol_aprobacion: {str(e)}")
        raise PruebaNotFoundError(str(e))


def listar_roles_aprobacion_listados(db: Session) -> list[Listados]:
    try:
        from entity.users import Users
        usuarios_db = db.query(Users).order_by(Users.first_name.asc()).all()
        lista_usuarios = [
            ListaGenerica(
                identity=u.id,
                valor=_full_name(u),
                valor_referencia=u.email,
                valor_referencia2=u.position,
            )
            for u in usuarios_db
        ]
        return [Listados(id_listado=0, tipo_listado='Usuarios', lista_generica=lista_usuarios)]
    except Exception as e:
        logging.error(f"Failed to list roles_aprobacion_listados: {str(e)}")
        raise PruebaNotFoundError(str(e))


def crear_rol_aprobacion(payload: RolesAprobacionBase, db: Session) -> ResponseRequest:
    try:
        rol = RolesAprobacion(
            nombre=payload.nombre,
            descripcion=payload.descripcion,
            activo=payload.activo if payload.activo is not None else True,
        )
        db.add(rol)
        db.commit()
        db.refresh(rol)
        _actualizar_usuarios_rol(rol.id_rol_aprobacion, payload.usuarios, db)
        return ResponseRequest(solicitud_exitosa=True, mensaje='Rol de aprobación creado correctamente', identity=rol.id_rol_aprobacion)
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create rol_aprobacion: {str(e)}")
        raise PruebaCreationError(str(e))


def actualizar_rol_aprobacion(role_id: int, payload: RolesAprobacionBase, db: Session) -> ResponseRequest:
    try:
        rol = db.query(RolesAprobacion).filter(RolesAprobacion.id_rol_aprobacion == role_id).first()
        if not rol:
            return ResponseRequest(solicitud_exitosa=False, mensaje='Rol de aprobación no encontrado')
        rol.nombre = payload.nombre
        rol.descripcion = payload.descripcion
        if payload.activo is not None:
            rol.activo = payload.activo
        db.commit()
        _actualizar_usuarios_rol(role_id, payload.usuarios, db)
        return ResponseRequest(solicitud_exitosa=True, mensaje='Rol de aprobación actualizado correctamente', identity=role_id)
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to update rol_aprobacion: {str(e)}")
        raise PruebaCreationError(str(e))


def _actualizar_usuarios_rol(id_rol: int, usuarios: list[RolesAprobacionUsuariosBase], db: Session) -> None:
    usuarios_actuales = db.query(RolesAprobacionUsuarios).filter(
        RolesAprobacionUsuarios.id_rol_aprobacion == id_rol
    ).all()
    ids_actuales = {u.id_usuario for u in usuarios_actuales}
    ids_nuevos = {u.id_usuario for u in usuarios if u.id_usuario is not None}

    for u in usuarios_actuales:
        if u.id_usuario not in ids_nuevos:
            u.activo = False

    for usuario in usuarios:
        if usuario.id_usuario is not None and usuario.id_usuario not in ids_actuales:
            db.add(RolesAprobacionUsuarios(
                id_rol_aprobacion=id_rol,
                id_usuario=usuario.id_usuario,
                activo=True,
            ))
    db.commit()


# ---------------------------------------------------------------------------
# Flujos de Aprobación
# ---------------------------------------------------------------------------

def listar_flujos_aprobacion(db: Session) -> list[FlujosAprobacionBase]:
    try:
        flujos_db = db.query(FlujosAprobacion).all()
        result = []
        for flujo in flujos_db:
            rutas = [
                FlujosAprobacionRutaBase(
                    id_ruta=r.id_ruta,
                    id_flujo_aprobacion=r.id_flujo_aprobacion,
                    id_rol_aprobacion=r.id_rol_aprobacion,
                    orden=r.orden,
                    activo=r.activo,
                    rol=r.rol.nombre if r.rol else None,
                    descripcion=r.rol.descripcion if r.rol else None,
                )
                for r in sorted(flujo.rutas, key=lambda x: x.orden or 0)
            ]
            result.append(FlujosAprobacionBase(
                id_flujo_aprobacion=flujo.id_flujo_aprobacion,
                nombre=flujo.nombre,
                descripcion=flujo.descripcion,
                activo=flujo.activo,
                categoria=flujo.categoria.nombre if flujo.categoria else None,
                id_categoria=flujo.id_categoria,
                rutas=rutas,
            ))
        return result
    except Exception as e:
        logging.error(f"Failed to list flujos_aprobacion: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_flujo_aprobacion_por_id(flow_id: int, db: Session) -> Optional[FlujosAprobacionBase]:
    try:
        flujo = db.query(FlujosAprobacion).filter(FlujosAprobacion.id_flujo_aprobacion == flow_id).first()
        if not flujo:
            return None
        rutas = [
            FlujosAprobacionRutaBase(
                id_ruta=r.id_ruta,
                id_flujo_aprobacion=r.id_flujo_aprobacion,
                id_rol_aprobacion=r.id_rol_aprobacion,
                orden=r.orden,
                activo=r.activo,
                rol=r.rol.nombre if r.rol else None,
                descripcion=r.rol.descripcion if r.rol else None,
            )
            for r in sorted(flujo.rutas, key=lambda x: x.orden or 0)
        ]
        return FlujosAprobacionBase(
            id_flujo_aprobacion=flujo.id_flujo_aprobacion,
            nombre=flujo.nombre,
            descripcion=flujo.descripcion,
            activo=flujo.activo,
            categoria=flujo.categoria.nombre if flujo.categoria else None,
            id_categoria=flujo.id_categoria,
            rutas=rutas,
        )
    except Exception as e:
        logging.error(f"Failed to get flujo_aprobacion: {str(e)}")
        raise PruebaNotFoundError(str(e))


def listar_flujos_aprobacion_listados(db: Session) -> list[Listados]:
    try:
        roles_db = db.query(RolesAprobacion).all()
        categorias_db = db.query(CategoriasAprobacion).all()
        lista_roles = [
            ListaGenerica(
                identity=r.id_rol_aprobacion,
                valor=r.nombre,
                valor_referencia=r.descripcion,
            )
            for r in roles_db
        ]
        lista_categorias = [
            ListaGenerica(
                identity=c.id_categoria,
                valor=c.nombre,
            )
            for c in categorias_db
        ]
        return [
            Listados(id_listado=0, tipo_listado='Roles de Aprobación', lista_generica=lista_roles),
            Listados(id_listado=1, tipo_listado='Categorías de Aprobación', lista_generica=lista_categorias),
        ]
    except Exception as e:
        logging.error(f"Failed to list flujos_aprobacion_listados: {str(e)}")
        raise PruebaNotFoundError(str(e))


def crear_flujo_aprobacion(payload: FlujosAprobacionBase, db: Session) -> ResponseRequest:
    try:
        flujo = FlujosAprobacion(
            nombre=payload.nombre,
            descripcion=payload.descripcion,
            id_categoria=payload.id_categoria,
            activo=payload.activo if payload.activo is not None else True,
        )
        db.add(flujo)
        db.commit()
        db.refresh(flujo)
        _actualizar_rutas_flujo(flujo.id_flujo_aprobacion, payload.rutas, db)
        return ResponseRequest(solicitud_exitosa=True, mensaje='Flujo creado correctamente', identity=flujo.id_flujo_aprobacion)
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create flujo_aprobacion: {str(e)}")
        raise PruebaCreationError(str(e))


def actualizar_flujo_aprobacion(flow_id: int, payload: FlujosAprobacionBase, db: Session) -> ResponseRequest:
    try:
        flujo = db.query(FlujosAprobacion).filter(FlujosAprobacion.id_flujo_aprobacion == flow_id).first()
        if not flujo:
            return ResponseRequest(solicitud_exitosa=False, mensaje='Flujo no encontrado')
        flujo.nombre = payload.nombre
        flujo.descripcion = payload.descripcion
        if payload.id_categoria is not None:
            flujo.id_categoria = payload.id_categoria
        if payload.activo is not None:
            flujo.activo = payload.activo
        db.commit()
        _actualizar_rutas_flujo(flow_id, payload.rutas, db)
        return ResponseRequest(solicitud_exitosa=True, mensaje='Flujo actualizado correctamente', identity=flow_id)
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to update flujo_aprobacion: {str(e)}")
        raise PruebaCreationError(str(e))


def _actualizar_rutas_flujo(id_flujo: int, rutas: list[FlujosAprobacionRutaBase], db: Session) -> None:
    rutas_actuales = db.query(FlujosAprobacionRuta).filter(
        FlujosAprobacionRuta.id_flujo_aprobacion == id_flujo
    ).all()
    ids_actuales = {r.id_ruta for r in rutas_actuales}
    ids_nuevos = {r.id_ruta for r in rutas if r.id_ruta is not None}

    for ruta in rutas_actuales:
        if ruta.id_ruta not in ids_nuevos:
            ruta.activo = False

    for ruta in rutas:
        if ruta.id_ruta is None or ruta.id_ruta not in ids_actuales:
            db.add(FlujosAprobacionRuta(
                id_flujo_aprobacion=id_flujo,
                id_rol_aprobacion=ruta.id_rol_aprobacion,
                orden=ruta.orden,
                activo=True,
            ))
    db.commit()


# ---------------------------------------------------------------------------
# Delegaciones (preserved for future use)
# ---------------------------------------------------------------------------

def listar_delegaciones_roles_usuarios(db: Session) -> list[DelegacionRolesUsuariosBase]:
    return []


def obtener_delegacion_roles_usuarios_por_id(delegation_id: int, db: Session) -> Optional[DelegacionRolesUsuariosBase]:
    return None


def listar_delegaciones_listados(delegation_id: int, db: Session) -> list[Listados]:
    return []


def crear_delegacion_roles_usuarios(payload: DelegacionRolesUsuariosBase, db: Session) -> ResponseRequest:
    return ResponseRequest(solicitud_exitosa=False, mensaje='No implementado')


def actualizar_delegacion_roles_usuarios(payload: DelegacionRolesUsuariosBase, db: Session) -> ResponseRequest:
    return ResponseRequest(solicitud_exitosa=False, mensaje='No implementado')

