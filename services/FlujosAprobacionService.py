import logging
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import join, or_
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
from entity.programs import Programs
from entity.approval_categories import ApprovalCategory
from entity.approval_flows import ApprovalFlow
from entity.approval_flow_steps import ApprovalFlowStep
from entity.approval_roles import ApprovalRole
from entity.approval_role_users import ApprovalRoleUser
from entity.vw_approval_flows import VWApprovalFlows
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
        roles_db = db.query(ApprovalRole).all()
        result = []
        for rol in roles_db:
            usuarios = []
            for u in rol.role_users:
                user = u.user
                usuarios.append(RolesAprobacionUsuariosBase(
                    id_rol_usuario=u.approval_role_user_id,
                    id_rol_aprobacion=u.approval_role_id,
                    id_usuario=u.user_id,
                    activo=u.active,
                    usuario=_full_name(user) if user else None,
                    correo=user.email if user else None,
                    area=user.position if user else None,
                ))
            result.append(RolesAprobacionBase(
                id_rol_aprobacion=rol.approval_role_id,
                nombre=rol.name,
                descripcion=rol.description,
                activo=rol.active,
                usuarios=usuarios,
            ))
        return result
    except Exception as e:
        logging.error(f"Failed to list roles_aprobacion: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_rol_aprobacion_por_id(role_id: int, db: Session) -> Optional[RolesAprobacionBase]:
    try:
        rol = db.query(ApprovalRole).filter(ApprovalRole.approval_role_id == role_id).first()
        if not rol:
            return None
        usuarios = []
        for u in rol.role_users:
            user = u.user
            usuarios.append(RolesAprobacionUsuariosBase(
                id_rol_usuario=u.approval_role_user_id,
                id_rol_aprobacion=u.approval_role_id,
                id_usuario=u.user_id,
                activo=u.active,
                usuario=_full_name(user) if user else None,
                correo=user.email if user else None,
                area=user.position if user else None,
            ))
        return RolesAprobacionBase(
            id_rol_aprobacion=rol.approval_role_id,
            nombre=rol.name,
            descripcion=rol.description,
            activo=rol.active,
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
        rol = ApprovalRole(
            name=payload.nombre,
            description=payload.descripcion,
            active=payload.activo if payload.activo is not None else True,
        )
        db.add(rol)
        db.commit()
        db.refresh(rol)
        _actualizar_usuarios_rol(rol.approval_role_id, payload.usuarios, db)
        return ResponseRequest(solicitud_exitosa=True, mensaje='Rol de aprobación creado correctamente', identity=rol.approval_role_id)
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create rol_aprobacion: {str(e)}")
        raise PruebaCreationError(str(e))


def actualizar_rol_aprobacion(role_id: int, payload: RolesAprobacionBase, db: Session) -> ResponseRequest:
    try:
        rol = db.query(ApprovalRole).filter(ApprovalRole.approval_role_id == role_id).first()
        if not rol:
            return ResponseRequest(solicitud_exitosa=False, mensaje='Rol de aprobación no encontrado')
        rol.name = payload.nombre
        rol.description = payload.descripcion
        if payload.activo is not None:
            rol.active = payload.activo
        db.commit()
        _actualizar_usuarios_rol(role_id, payload.usuarios, db)
        return ResponseRequest(solicitud_exitosa=True, mensaje='Rol de aprobación actualizado correctamente', identity=role_id)
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to update rol_aprobacion: {str(e)}")
        raise PruebaCreationError(str(e))


def _actualizar_usuarios_rol(id_rol: int, usuarios: list[RolesAprobacionUsuariosBase], db: Session) -> None:
    usuarios_actuales = db.query(ApprovalRoleUser).filter(
        ApprovalRoleUser.approval_role_id == id_rol
    ).all()
    ids_actuales = {u.user_id for u in usuarios_actuales}
    ids_nuevos = {u.id_usuario for u in usuarios if u.id_usuario is not None}

    for u in usuarios_actuales:
        if u.user_id not in ids_nuevos:
            u.active = False

    for usuario in usuarios:
        if usuario.id_usuario is not None and usuario.id_usuario not in ids_actuales:
            db.add(ApprovalRoleUser(
                approval_role_id=id_rol,
                user_id=usuario.id_usuario,
                active=True,
            ))
    db.commit()


# ---------------------------------------------------------------------------
# Flujos de Aprobación
# ---------------------------------------------------------------------------

def listar_flujos_aprobacion(db: Session) -> list[FlujosAprobacionBase]:
    try:
        flujos_db = db.query(ApprovalFlow).all()
        result = []
        for flujo in flujos_db:
            rutas = [
                FlujosAprobacionRutaBase(
                    id_ruta=r.step_id,
                    id_flujo_aprobacion=r.approval_flow_id,
                    id_rol_aprobacion=r.approval_role_id,
                    orden=r.step_order,
                    activo=r.active,
                    rol=r.approval_role.name if r.approval_role else None,
                    descripcion=r.approval_role.description if r.approval_role else None,
                )
                for r in sorted(flujo.steps, key=lambda x: x.step_order or 0)
            ]
            result.append(FlujosAprobacionBase(
                id_flujo_aprobacion=flujo.approval_flow_id,
                nombre=flujo.name,
                descripcion=flujo.description,
                activo=flujo.active,
                categoria=flujo.category.name if flujo.category else None,
                id_categoria=flujo.category_id if flujo.category else None,
                rutas=rutas,
                id_programa=flujo.program_id if flujo.program_id else None,
                programa=flujo.program.name if flujo.program else None,
            ))
        return result
    except Exception as e:
        logging.error(f"Failed to list flujos_aprobacion: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_flujo_aprobacion_por_id(flow_id: int, db: Session) -> Optional[FlujosAprobacionBase]:
    try:
        flujo = db.query(ApprovalFlow).filter(ApprovalFlow.approval_flow_id == flow_id).first()
        if not flujo:
            return None
        rutas = [
            FlujosAprobacionRutaBase(
                id_ruta=r.step_id,
                id_flujo_aprobacion=r.approval_flow_id,
                id_rol_aprobacion=r.approval_role_id,
                orden=r.step_order,
                activo=r.active,
                rol=r.approval_role.name if r.approval_role else None,
                descripcion=r.approval_role.description if r.approval_role else None,
            )
            for r in sorted(flujo.steps, key=lambda x: x.step_order or 0)
        ]
        return FlujosAprobacionBase(
            id_flujo_aprobacion=flujo.approval_flow_id,
            nombre=flujo.name,
            descripcion=flujo.description,
            activo=flujo.active,
            categoria=flujo.category.name if flujo.category else None,
            id_categoria=flujo.category_id if flujo.category else None,
            rutas=rutas,
            id_programa=flujo.program_id if flujo.program_id is not None else None
        )
    except Exception as e:
        logging.error(f"Failed to get flujo_aprobacion: {str(e)}")
        raise PruebaNotFoundError(str(e))


def listar_flujos_aprobacion_listados(db: Session) -> list[Listados]:
    try:
        roles_db = db.query(ApprovalRole).all()
        categorias_db = db.query(ApprovalCategory).all()
        programas_db = db.query(Programs).all()

        listados = []
        lista_catalogos = []

        lista_catalogos = [
            ListaGenerica(
                identity=r.approval_role_id,
                valor=r.name,
                valor_referencia=r.description,
            )
            for r in roles_db
        ]

        listados.append(
            Listados(
                id_listado=0, 
                tipo_listado="Roles de Aprobación", 
                lista_generica=lista_catalogos
            )
        )

        lista_catalogos = []

        lista_catalogos = [
            ListaGenerica(
                identity=c.category_id,
                valor=c.name,
                valor_referencia=c.description,
            )
            for c in categorias_db
        ]

        listados.append(
            Listados(
                id_listado=1, 
                tipo_listado="Categorías de Aprobación", 
                lista_generica=lista_catalogos
            )
        )


        lista_catalogos = []

        lista_catalogos = [
            ListaGenerica(
                identity=p.id,
                valor=p.name,
            )
            for p in programas_db
        ]

        listados.append(
            Listados(
                id_listado=1, 
                tipo_listado="Programas", 
                lista_generica=lista_catalogos
            )
        )
        
        return listados
    except Exception as e:
        logging.error(f"Failed to list flujos_aprobacion_listados: {str(e)}")
        raise PruebaNotFoundError(str(e))


def crear_flujo_aprobacion(payload: FlujosAprobacionBase, db: Session) -> ResponseRequest:
    try:
        flujo = ApprovalFlow(
            name=payload.nombre,
            description=payload.descripcion,
            category_id=payload.id_categoria,
            active=payload.activo if payload.activo is not None else True,
            program_id=payload.id_programa
        )
        db.add(flujo)
        db.commit()
        db.refresh(flujo)
        _actualizar_rutas_flujo(flujo.approval_flow_id, payload.rutas, db)
        return ResponseRequest(solicitud_exitosa=True, mensaje='Flujo creado correctamente', identity=flujo.approval_flow_id)
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create flujo_aprobacion: {str(e)}")
        raise PruebaCreationError(str(e))


def actualizar_flujo_aprobacion(flow_id: int, payload: FlujosAprobacionBase, db: Session) -> ResponseRequest:
    try:
        flujo = db.query(ApprovalFlow).filter(ApprovalFlow.approval_flow_id == flow_id).first()
        if not flujo:
            return ResponseRequest(solicitud_exitosa=False, mensaje='Flujo no encontrado')
        flujo.name = payload.nombre
        flujo.description = payload.descripcion
        if payload.id_categoria is not None:
            flujo.category_id = payload.id_categoria
        if payload.activo is not None:
            flujo.active = payload.activo
        if payload.id_programa is not None:
            flujo.program_id = payload.id_programa
        db.commit()
        _actualizar_rutas_flujo(flow_id, payload.rutas, db)
        return ResponseRequest(solicitud_exitosa=True, mensaje='Flujo actualizado correctamente', identity=flow_id)
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to update flujo_aprobacion: {str(e)}")
        raise PruebaCreationError(str(e))


def _actualizar_rutas_flujo(id_flujo: int, rutas: list[FlujosAprobacionRutaBase], db: Session) -> None:
    rutas_actuales = db.query(ApprovalFlowStep).filter(
        ApprovalFlowStep.approval_flow_id == id_flujo
    ).all()
    ids_actuales = {r.step_id for r in rutas_actuales}
    ids_nuevos = {r.id_ruta for r in rutas if r.id_ruta is not None}

    for ruta in rutas_actuales:
        if ruta.step_id not in ids_nuevos:
            ruta.active = False

    for ruta in rutas:
        if ruta.id_ruta is None or ruta.id_ruta not in ids_actuales:
            db.add(ApprovalFlowStep(
                approval_flow_id=id_flujo,
                approval_role_id=ruta.id_rol_aprobacion,
                step_order=ruta.orden,
                active=True,
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


def obtener_flujo_aprobacion_x_categoria_x_usuario_inicio_flujo(id_categoria: int, id_usuario: int, db: Session, id_programa: int = None) -> tuple:
    try:
        print("id_categoria", id_categoria)
        print("id_usuario", id_usuario)
        flujos_aprobacionDB = db.query(VWApprovalFlows).filter(
            VWApprovalFlows.category_id == id_categoria,
            VWApprovalFlows.flow_active == True,
            VWApprovalFlows.user_id == id_usuario,
            VWApprovalFlows.user_role_active == True,
            VWApprovalFlows.step_active == True,
            VWApprovalFlows.role_active == True,
            VWApprovalFlows.step_order == 1,
            VWApprovalFlows.program_id == id_programa
        ).first()

        if not flujos_aprobacionDB:
            return None, None, None, None
        else:
            return flujos_aprobacionDB.approval_flow_id, flujos_aprobacionDB.category, flujos_aprobacionDB.approval_role_id, flujos_aprobacionDB.step_id
            # return flujos_aprobacionDB.id_flujo_aprobacion, flujos_aprobacionDB.categoria, flujos_aprobacionDB.id_rol_aprobacion, flujos_aprobacionDB.id_ruta

    except Exception as e:
        logging.error(f"Failed to list roles: {str(e)}")
        raise PruebaNotFoundError(str(e))
    


def obtener_siguiente_paso_ruta(id_categoria: int, paso_actual: int, id_flujo_aprobacion: int, db: Session) -> tuple:
    try:
        flujos_aprobacionDB = db.query(VWApprovalFlows).filter(
            VWApprovalFlows.category_id == id_categoria,
            VWApprovalFlows.flow_active == True,
            VWApprovalFlows.user_role_active == True,
            VWApprovalFlows.step_active == True,
            VWApprovalFlows.role_active == True,
            VWApprovalFlows.step_order == paso_actual + 1,
            VWApprovalFlows.approval_flow_id == id_flujo_aprobacion
        ).first()
        if not flujos_aprobacionDB:
            return None, None, None
        else:
            return flujos_aprobacionDB.approval_role_id, flujos_aprobacionDB.step_id, flujos_aprobacionDB.is_supervisor

    except Exception as e:
        logging.error(f"Failed to list roles: {str(e)}")
        raise PruebaNotFoundError(str(e))
    
def obtener_flujo_aprobacion_ruta_orden(id_categoria: int, id_usuario: int, orden: int, id_flujo_aprobacion: int, db: Session) -> VWApprovalFlows:
    try:
        print("id_usuario -> ", id_usuario)
        print("orden -> ", orden)
        print("id_flujo_aprobacion -> ", id_flujo_aprobacion)
        flujos_aprobacionDB = db.query(VWApprovalFlows).filter(
            VWApprovalFlows.category_id == id_categoria,
            VWApprovalFlows.flow_active == True,
            or_(
                VWApprovalFlows.user_id == id_usuario
                # ,
                # VWApprovalFlows.delegated_user_ids.any(id_usuario)
            ),
            VWApprovalFlows.user_role_active == True,
            VWApprovalFlows.step_active == True,
            VWApprovalFlows.role_active == True,
            VWApprovalFlows.step_order == orden,
            VWApprovalFlows.approval_flow_id == id_flujo_aprobacion
        ).first()
        if not flujos_aprobacionDB:
            return None
        else:
            return flujos_aprobacionDB

    except Exception as e:
        logging.error(f"Failed to list obtener_flujo_aprobacion_ruta_orden: {str(e)}")
        raise PruebaNotFoundError(str(e))    

def obtener_flujo_aprobacion_pasos(id_flujo_aprobacion: int, db: Session) -> int:
    flujoRuta = db.query(ApprovalFlowStep).filter(
        ApprovalFlowStep.approval_flow_id == id_flujo_aprobacion,
        ApprovalFlowStep.active == True
    ).order_by(ApprovalFlowStep.step_order.desc()).first()

    if not flujoRuta:
        return 0

    return flujoRuta.step_order



def obtener_rol_solicitud_ajuste(id_categoria: int, id_flujo_aprobacion: int, id_rol_aprobacion: int, id_usuario: int, db: Session) -> tuple:
    try:
        flujos_aprobacionDB = db.query(VWApprovalFlows).filter(
            VWApprovalFlows.category_id == id_categoria,
            VWApprovalFlows.flow_active == True,
            VWApprovalFlows.user_role_active == True,
            VWApprovalFlows.step_active == True,
            VWApprovalFlows.role_active == True,
            VWApprovalFlows.approval_flow_id == id_flujo_aprobacion,
            VWApprovalFlows.approval_role_id == id_rol_aprobacion,
            VWApprovalFlows.user_id == id_usuario
        ).first()
        if not flujos_aprobacionDB:
            return None, None, None, None
        else:
            return flujos_aprobacionDB.approval_role_id, flujos_aprobacionDB.step_id, flujos_aprobacionDB.is_supervisor, flujos_aprobacionDB.step_order

    except Exception as e:
        logging.error(f"Failed to list roles: {str(e)}")
        raise PruebaNotFoundError(str(e))