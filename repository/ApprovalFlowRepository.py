from sqlalchemy.orm import Session
from sqlalchemy import desc

from entity.approval_flow_steps import ApprovalFlowStep

def obtener_paso_requiere_ajuste(flujo_aprobacion_id: int, id_rol: int, paso_actual: int, db: Session) -> ApprovalFlowStep | None:
    paso_requiere_ajuste = (
        db.query(ApprovalFlowStep)
        .filter(
            ApprovalFlowStep.approval_flow_id == flujo_aprobacion_id,
            ApprovalFlowStep.approval_role_id == id_rol,
            ApprovalFlowStep.step_order < (paso_actual or 0),
            ApprovalFlowStep.active == True,
        )
        .order_by(desc(ApprovalFlowStep.step_order))
        .first()
    )
    return paso_requiere_ajuste