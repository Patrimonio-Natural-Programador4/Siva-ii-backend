from entity.approval_request_history import ApprovalRequestHistory
from entity.vw_approval_request_history import VWApprovalRequestHistory
import logging
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, func

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