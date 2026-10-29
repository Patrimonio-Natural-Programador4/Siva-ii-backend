from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

"""
class PreviousStudiesFlowItem(BaseModel):
    approval_request_id: Optional[int] = None
    code: Optional[str] = None
    rol: Optional[str] = None
    implementadora: Optional[str] = None
    fecha_crea: Optional[datetime] = None
    fecha_aprobacion: Optional[datetime] = None
    pilar: Optional[str] = None
    lider_pilar: Optional[str] = None
    usuario: Optional[str] = None
    id_programa : Optional[int] = None
    programa: Optional[str] = None
    tipo_convenio: Optional[str] = None
    modalidad: Optional[str] = None
    estado_aprobacion: Optional[str] = None
    step_order: Optional[int] = None
    previous_study_id: Optional[int] = None
    capacity_assessment_id: Optional[int] = None
    guid_ev: Optional[UUID] = None
    modalidad_id: Optional[int] = None
    id_capacity_state_id: Optional[int] = None
    capacity_state: Optional[str] = None

    class Config:
        from_attributes = True
"""

class PreviousStudiesFlowItem(BaseModel):
    approval_request_id: Optional[int] = None
    code_agreements: Optional[str] = None
    rol: Optional[str] = None
    iep_implementer_id: Optional[int] = None
    implementadora: Optional[str] = None
    fecha_crea: Optional[datetime] = None
    fecha_aprobacion: Optional[datetime] = None
    pilar: Optional[str] = None
    lider_pilar: Optional[str] = None
    usuario: Optional[str] = None
    id_programa: Optional[int] = None
    ep_agreement_type_id: Optional[int] = None
    programa: Optional[str] = None
    tipo_convenio: Optional[str] = None
    modalidad_id: Optional[int] = None
    modalidad: Optional[str] = None
    estado_aprobacion: Optional[str] = None
    step_order: Optional[int] = None
    previous_study_id: Optional[int] = None
    guid_ev: Optional[UUID] = None
    ep_precedents: Optional[str] = None
    ep_justification: Optional[str] = None
    ep_scope: Optional[str] = None
    ep_overall_objective: Optional[str] = None
    ep_term: Optional[str] = None
    ep_obligations: Optional[str] = None
    ep_supervisor: Optional[str] = None
    ep_create_date: Optional[datetime] = None
    ep_total_value: Optional[Decimal] = None
    ep_contributions_ei: Optional[Decimal] = None
    ep_total_value_executes_fpn: Optional[Decimal] = None
    ep_total_value_executes_ei: Optional[Decimal] = None
    ep_persons_email: Optional[str] = None
    ep_persons_id: Optional[int] = None
    capacity_assessment_id: Optional[int] = None
    ep_capacity_assessment: Optional[str] = None
    ep_aproval_request: Optional[str] = None
    ep_approval_request_id: Optional[int] = None
    id_capacity_state_id: Optional[int] = None
    capacity_state: Optional[str] = None
    codde: Optional[str] = None

    class Config:
        from_attributes = True

class PreviousStudiesFlowPage(BaseModel):
    items: List[PreviousStudiesFlowItem] = []
    total: int = 0
    page: int = 1
    page_size: int = 10