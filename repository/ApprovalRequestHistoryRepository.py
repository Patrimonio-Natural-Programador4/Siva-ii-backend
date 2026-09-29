from entity.approval_request_history import ApprovalRequestHistory
from entity.vw_approval_request_history import VWApprovalRequestHistory
from entity.approval_flow_steps import ApprovalFlowStep
from entity.approval_roles import ApprovalRole
from entity.approval_role_users import ApprovalRoleUser
from entity.users import Users
from entity.vw_approval_flows import VWApprovalFlows
import logging
from sqlalchemy.orm import Session
from sqlalchemy import and_, asc, desc, func, or_


def obtener_asignaciones_revisor(id_solicitud_aprobacion: int, id_flujo_aprobacion: int, db: Session):
    return (
        db.query(ApprovalRequestHistory, ApprovalFlowStep, ApprovalRole)
        .join(ApprovalFlowStep, ApprovalFlowStep.step_id == ApprovalRequestHistory.step_id)
        .join(ApprovalRole, ApprovalRole.approval_role_id == ApprovalRequestHistory.approval_role_id)
        .filter(
            ApprovalRequestHistory.approval_request_id == id_solicitud_aprobacion,
            ApprovalRequestHistory.approval_status_id == 6,
            ApprovalFlowStep.approval_flow_id == id_flujo_aprobacion,
            ApprovalFlowStep.active == True,
            ApprovalFlowStep.assign_reviewer == True,
            ApprovalRole.active == True,
        )
        .order_by(ApprovalFlowStep.step_order.asc(), ApprovalRequestHistory.history_id.asc())
        .all()
    )


def usuario_es_miembro_rol(id_rol_aprobacion: int, id_usuario: int, db: Session) -> bool:
    return db.query(ApprovalRoleUser.approval_role_user_id).filter(
        ApprovalRoleUser.approval_role_id == id_rol_aprobacion,
        ApprovalRoleUser.user_id == id_usuario,
        ApprovalRoleUser.active == True,
    ).first() is not None


def listar_usuarios_activos_rol(id_rol_aprobacion: int, db: Session) -> list[Users]:
    return (
        db.query(Users)
        .join(ApprovalRoleUser, ApprovalRoleUser.user_id == Users.id)
        .filter(
            ApprovalRoleUser.approval_role_id == id_rol_aprobacion,
            ApprovalRoleUser.active == True,
            Users.is_active == True,
        )
        .order_by(Users.first_name.asc(), Users.last_name.asc())
        .all()
    )


def obtener_historial_por_id(history_id: int, db: Session, bloquear: bool = False) -> ApprovalRequestHistory | None:
    query = db.query(ApprovalRequestHistory).filter(
        ApprovalRequestHistory.history_id == history_id
    )
    if bloquear:
        query = query.with_for_update()
    return query.first()


def obtener_paso_revisor(step_id: int, db: Session) -> ApprovalFlowStep | None:
    return db.query(ApprovalFlowStep).filter(
        ApprovalFlowStep.step_id == step_id,
        ApprovalFlowStep.active == True,
        ApprovalFlowStep.assign_reviewer == True,
    ).first()


def usuario_asignable_rol(id_rol_aprobacion: int, id_usuario: int, db: Session) -> Users | None:
    return (
        db.query(Users)
        .join(ApprovalRoleUser, ApprovalRoleUser.user_id == Users.id)
        .filter(
            ApprovalRoleUser.approval_role_id == id_rol_aprobacion,
            ApprovalRoleUser.user_id == id_usuario,
            ApprovalRoleUser.active == True,
            Users.is_active == True,
        )
        .first()
    )


def obtener_ruta_pendiente_usuario(
    id_solicitud_aprobacion: int,
    id_categoria: int,
    id_usuario: int,
    orden: int,
    id_flujo_aprobacion: int,
    db: Session,
) -> list[tuple[VWApprovalRequestHistory, ApprovalRequestHistory]]:
    return (
        db.query(VWApprovalFlows, ApprovalRequestHistory)
        .select_from(VWApprovalFlows)
        .join(
            VWApprovalRequestHistory,
            and_(
                VWApprovalRequestHistory.approval_request_id == id_solicitud_aprobacion,
                VWApprovalRequestHistory.approval_workflow_id == id_flujo_aprobacion,
                VWApprovalRequestHistory.step_id == VWApprovalFlows.step_id,
            ),
        )
        .join(
            ApprovalRequestHistory,
            ApprovalRequestHistory.history_id == VWApprovalRequestHistory.history_id,
        )
        .filter(
            VWApprovalRequestHistory.category_id == id_categoria,
            VWApprovalRequestHistory.step_order == orden,
            VWApprovalRequestHistory.approval_status_step_id == 6,
            VWApprovalFlows.user_id == id_usuario,
            VWApprovalFlows.approval_flow_id == id_flujo_aprobacion,
            VWApprovalFlows.flow_active == True,
            VWApprovalFlows.step_active == True,
            VWApprovalFlows.role_active == True,
            VWApprovalFlows.user_role_active == True,
            or_(
                ApprovalRequestHistory.user_id == id_usuario,
                and_(ApprovalRequestHistory.user_id.is_(None), VWApprovalFlows.is_supervisor == False),
            ),
        )
        .order_by(VWApprovalFlows.step_id.asc(), VWApprovalRequestHistory.history_id.asc())
        .all()
    )


def listar_pasos_aprobables_orden(id_flujo_aprobacion: int, orden: int, db: Session) -> list[ApprovalFlowStep]:
    return (
        db.query(ApprovalFlowStep)
        .join(VWApprovalFlows, VWApprovalFlows.step_id == ApprovalFlowStep.step_id)
        .filter(
            ApprovalFlowStep.approval_flow_id == id_flujo_aprobacion,
            ApprovalFlowStep.step_order == orden,
            ApprovalFlowStep.active == True,
            VWApprovalFlows.flow_active == True,
            VWApprovalFlows.step_active == True,
            VWApprovalFlows.role_active == True,
            VWApprovalFlows.user_role_active == True,
        )
        .distinct()
        .all()
    )

def obtener_historial_por_registro_asociado_categoria(id_registro_asociado: int, id_categoria: int, db: Session) -> list[VWApprovalRequestHistory] | None:
    try:
        solicitudHistorial = (
            db.query(VWApprovalRequestHistory)
            .filter(
                VWApprovalRequestHistory.related_record_id == id_registro_asociado,
                VWApprovalRequestHistory.category_id == id_categoria
            )
            .order_by(
                asc(
                    func.coalesce(
                        VWApprovalRequestHistory.approved_at,
                        VWApprovalRequestHistory.created_at
                    )
                )
            )
            .all()
        )
        return solicitudHistorial
    except Exception as e:
        logging.error(f"Failed to get historial por registro asociado y categoria: {str(e)}")
        raise Exception(str(e))

def obtener_historial_ultima_aprobacion(id_registro_asociado: int, id_categoria: int, db: Session) -> VWApprovalRequestHistory | None:
    try:
        historial = db.query(VWApprovalRequestHistory).filter(
            VWApprovalRequestHistory.related_record_id == id_registro_asociado,
            VWApprovalRequestHistory.category_id == id_categoria
        ).order_by(VWApprovalRequestHistory.history_id.desc()).first()
        return historial
    except Exception as e:
        logging.error(f"Failed to get historial por registro asociado y categoria: {str(e)}")
        raise Exception(str(e))    

def obtener_historial_ultimas_dos_aprobaciones(id_registro_asociado: int, id_categoria: int, db: Session) -> list[VWApprovalRequestHistory] | None:
    try:
        historial = db.query(VWApprovalRequestHistory).filter(
                        VWApprovalRequestHistory.related_record_id == id_registro_asociado,
                        VWApprovalRequestHistory.category_id == id_categoria
                    ).order_by(VWApprovalRequestHistory.step_order.desc()).limit(2).all()
        return historial
    except Exception as e:
        logging.error(f"Failed to get historial por registro asociado y categoria: {str(e)}")
        raise Exception(str(e))        

def obtener_historial_aprovaciones_previas_pendientes(id_solicitud_aprobacion: int, orden: int, estados: list[int], db: Session) -> list[VWApprovalRequestHistory] | None:
    try:
        historial = db.query(VWApprovalRequestHistory).filter(
            VWApprovalRequestHistory.approval_request_id == id_solicitud_aprobacion,
            VWApprovalRequestHistory.step_order < orden,
            VWApprovalRequestHistory.approval_status_id.in_(estados)
        ).all()
        return historial
    except Exception as e:
        logging.error(f"Failed to get historial de aprobaciones previas pendientes: {str(e)}")
        raise Exception(str(e))

def obtener_historial_ultima_accion(id_solicitud_aprobacion: int, identity: int, id_categoria: int, db: Session) -> VWApprovalRequestHistory | None:
    try:
        historial = db.query(VWApprovalRequestHistory).filter(
            VWApprovalRequestHistory.approval_request_id == id_solicitud_aprobacion,
            VWApprovalRequestHistory.related_record_id == identity,
            VWApprovalRequestHistory.category_id == id_categoria
        ).order_by(VWApprovalRequestHistory.history_id.desc()).first()
        return historial
    except Exception as e:
        logging.error(f"Failed to get historial de aprobaciones previas pendientes: {str(e)}")
        raise Exception(str(e))  

def obtener_ruta(id_solicitud_aprobacion: int, id_estado_aprobacion: int, db: Session) -> ApprovalRequestHistory | None:
    try:
        ruta = db.query(ApprovalRequestHistory).filter(
                ApprovalRequestHistory.approval_request_id == id_solicitud_aprobacion,
                ApprovalRequestHistory.approval_status_id == id_estado_aprobacion
            ).order_by(ApprovalRequestHistory.history_id.desc()).first()
        return ruta
    except Exception as e:
        logging.error(f"Failed to get historial de aprobaciones previas pendientes: {str(e)}")
        raise Exception(str(e))        

def obtener_ruta_pendiente_por_paso(id_solicitud_aprobacion: int, id_paso: int, db: Session) -> ApprovalRequestHistory | None:
    return (
        db.query(ApprovalRequestHistory)
        .filter(
            ApprovalRequestHistory.approval_request_id == id_solicitud_aprobacion,
            ApprovalRequestHistory.step_id == id_paso,
            ApprovalRequestHistory.approval_status_id == 6,
        )
        .order_by(desc(ApprovalRequestHistory.history_id))
        .first()
    )

def obtener_historial_orden(id_solicitud_aprobacion: int, orden: int, db: Session) -> list[VWApprovalRequestHistory]:
    return (
        db.query(VWApprovalRequestHistory)
        .filter(
            VWApprovalRequestHistory.approval_request_id == id_solicitud_aprobacion,
            VWApprovalRequestHistory.step_order == orden,
        )
        .populate_existing()
        .order_by(VWApprovalRequestHistory.history_id.asc())
        .all()
    )

def obtener_historial_por_solicitud(id_solicitud_aprobacion: int, db: Session) -> list[VWApprovalRequestHistory]:
    return (
        db.query(VWApprovalRequestHistory)
        .filter(VWApprovalRequestHistory.approval_request_id == id_solicitud_aprobacion)
        .order_by(VWApprovalRequestHistory.history_id.asc())
        .all()
    )

def obtener_usuarios_disponibles_ajuste(id_solicitud_aprobacion: int, paso_actual: int, db: Session) -> list[VWApprovalRequestHistory]:
    historial = (
        db.query(VWApprovalRequestHistory)
        .filter(
            VWApprovalRequestHistory.approval_request_id == id_solicitud_aprobacion,
            VWApprovalRequestHistory.step_order < paso_actual,
            VWApprovalRequestHistory.user_id.is_not(None),
        )
        .order_by(VWApprovalRequestHistory.step_order.asc(), VWApprovalRequestHistory.history_id.asc())
        .all()
    )
    return historial

def obtener_historiales_pendientes(id_solicitud_aprobacion: int, db: Session) -> list[VWApprovalRequestHistory]:
    return (
        db.query(VWApprovalRequestHistory)
        .filter(
            VWApprovalRequestHistory.approval_request_id == id_solicitud_aprobacion,
            VWApprovalRequestHistory.approval_status_step_id == 6,
        )
        .order_by(VWApprovalRequestHistory.history_id.asc())
        .all()
    )