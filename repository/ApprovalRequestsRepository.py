from sqlalchemy.orm import Session
from sqlalchemy import desc
from entity.approval_requests import ApprovalRequests

def obtener_solicitud_por_registro_categoria(id_registro_asociado: int, db: Session) -> ApprovalRequests | None:
    return (
        db.query(ApprovalRequests)
        .filter(ApprovalRequests.related_record_id == id_registro_asociado)
        .order_by(desc(ApprovalRequests.approval_request_id))
        .first()
    )

def obtener_solicitud(id_solicitud_aprobacion: int, db: Session) -> ApprovalRequests | None:
    return db.query(ApprovalRequests).filter(
                ApprovalRequests.approval_request_id == id_solicitud_aprobacion
            ).first()