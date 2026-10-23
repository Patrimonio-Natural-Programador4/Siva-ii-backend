from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


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
    programa: Optional[str] = None
    tipo_convenio: Optional[str] = None
    modalidad: Optional[str] = None
    estado_aprobacion: Optional[str] = None
    step_order: Optional[int] = None
    previous_study_id: Optional[int] = None
    capacity_assessment_id: Optional[int] = None
    guid_ev: Optional[UUID] = None

    class Config:
        from_attributes = True


class PreviousStudiesFlowPage(BaseModel):
    items: List[PreviousStudiesFlowItem] = []
    total: int = 0
    page: int = 1
    page_size: int = 10