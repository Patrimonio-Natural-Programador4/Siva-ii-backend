from datetime import date, datetime
from typing import Optional
import decimal
import uuid
from pydantic import BaseModel

class AgreementsBase(BaseModel): 
    id: Optional[int] = None
    codigo_siva: Optional[str] = None
    nombre_convenio: Optional[str] = None
    objeto_acuerdo: Optional[str] = None
    prioridad_acuerdo: Optional[str] = None
    ano_ejecucion: Optional[int] = None
    monto_apropiado: Optional[decimal.Decimal] = None
    monto_total_apropiado: Optional[decimal.Decimal] = None
    total_paa: Optional[decimal.Decimal] = None

    class Config:
        from_attributes = True

class AgreementsFilterDTO(BaseModel):
    p_agreement_id: Optional[int] = None
    p_type_ids: Optional[list[int]] = None
    p_modality_ids: Optional[list[int]] = None
    p_core_ids: Optional[list[int]] = None
    p_pillar_ids: Optional[list[int]] = None
    p_years: Optional[list[int]] = None
    p_phase: Optional[list[str]] = None
    p_stage_ids: Optional[list[int]] = None
    p_priority: Optional[list[str]] = None
    p_alert: Optional[list[str]] = None
    p_search: Optional[str] = None
    p_page: Optional[int] = 1
    p_page_size: Optional[int] = 25

    class Config:
        from_attributes = True

class AgreementsListSP(BaseModel):
    id: Optional[int] = None
    codigo_siva: Optional[str] = None
    nombre_convenio: Optional[str] = None
    objeto_acuerdo: Optional[str] = None
    prioridad_acuerdo: Optional[str] = None
    ano_ejecucion: Optional[int] = None
    estado_name: Optional[str] = None
    estado_stage: Optional[str] = None
    estado_status: Optional[str] = None
    estado_color: Optional[str] = None
    tipo_name: Optional[str] = None
    tipo_color: Optional[str] = None
    modalidad_name: Optional[str] = None
    pilar_name: Optional[str] = None
    pilar_color: Optional[str] = None
    nucleos: Optional[str] = None
    implementadoras: Optional[str] = None
    monto_apropiado: Optional[decimal.Decimal] = None
    monto_total_apropiado: Optional[decimal.Decimal] = None
    total_paa: Optional[decimal.Decimal] = None
    total_registros: Optional[int] = None

    class Config:
        from_attributes = True
        
# Alias para responder a la importación del controller
#AgreementsCreate = AgreementCreate