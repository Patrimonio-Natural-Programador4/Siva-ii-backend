from entity.approval_request_history import ApprovalRequestHistory
from entity.vw_approval_request_history import VWApprovalRequestHistory
from entity.approval_flow_steps import ApprovalFlowStep
from entity.approval_roles import ApprovalRole
from entity.approval_role_users import ApprovalRoleUser
from entity.users import Users
from entity.vw_approval_flows import VWApprovalFlows
import logging
from sqlalchemy.orm import Session,aliased
from sqlalchemy import and_, asc, desc, func, or_
from sqlalchemy import text



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
#########################################################



QUERY_FLUJO_ESTUDIOS_PREVIOS = text("""
SELECT f.*
FROM (
    SELECT DISTINCT ON (a.approval_request_id)
           a.approval_request_id,
           a.code                                       AS code_agreements,
           h.rol                                       AS rol,
           im.name                                     AS implementadora,
           h.created_at                                AS fecha_crea,
           h.approved_at                               AS fecha_aprobacion,
           pi.name                                     AS pilar,
           concat_ws(' ', pe.first_name, pe.last_name) AS lider_pilar,
           COALESCE(h."user", resp.responsables)       AS usuario,
		   pr.id 									   AS id_programa,
           pr.name                                     AS programa,
           at.name                                     AS tipo_convenio,
		   mo.id									   AS modalidad_id,
           mo.name                                     AS modalidad,
           h.approval_route_status                     AS estado_aprobacion,
           h.step_order,
           ps.id                                       AS previous_study_id,
           ca.id                                       AS capacity_assessment_id,
           ps.guid                                     AS guid_ev,
		   caes.id 									   AS id_capacity_state_id,
		   caes.state 								   AS capacity_state,
            ps.code									   AS codde
    FROM approval_requests a
    INNER JOIN vw_approval_request_history h ON h.approval_request_id = a.approval_request_id
    INNER JOIN previous_studies ps           ON ps.approval_request_id = a.approval_request_id
    INNER JOIN capacity_assessments ca       ON ca.id = ps.capacity_assessment_id
	INNER JOIN capacity_assessments_states caes   ON caes.id = ca.capacity_assessments_states_id
    LEFT  JOIN implementers im               ON im.id = ps.implementer_id
    LEFT  JOIN programs pr                   ON pr.id = ps.program_id
    LEFT  JOIN pillars pi                    ON pi.id = ca.pillar_id
    LEFT  JOIN persons pe                    ON pe.id = pi.person_id
    LEFT  JOIN agreement_types at            ON at.id = ps.agreement_type_id
    LEFT  JOIN modalities mo                 ON mo.id = ps.modality_id
    LEFT  JOIN LATERAL (
        SELECT string_agg(
                   UPPER(concat_ws(' ', u.first_name, NULLIF(u.other_name, ''), u.last_name)),
                   ', ' ORDER BY u.first_name, u.last_name
               ) AS responsables
        FROM approval_role_users aru
        JOIN users u ON u.id = aru.user_id
        WHERE aru.approval_role_id = h.approval_role_id
    ) resp ON true
    ORDER BY a.approval_request_id, h.history_id DESC
) f
ORDER BY f.approval_request_id DESC;   
""")
#############################################################

def listar_flujo_estudios_previos(db: Session) -> list[dict]:
    rows = db.execute(QUERY_FLUJO_ESTUDIOS_PREVIOS).mappings().all()
    return [dict(r) for r in rows]
#############################################################

#########################################################
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


def listar_historial(db: Session) -> list[VWApprovalRequestHistory]:
    try:
        subq = (
            db.query(VWApprovalRequestHistory)
            .distinct(VWApprovalRequestHistory.guid)
            .order_by(
                VWApprovalRequestHistory.guid,
                desc(VWApprovalRequestHistory.created_at)
            )
            .subquery()
        )

        historial = aliased(VWApprovalRequestHistory, subq)
        return (
            db.query(historial)
            .order_by(asc(historial.created_at))
            .all()
        )
    except Exception as e:
        logging.error(f"Failed to listar historial: {str(e)}")
        raise


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