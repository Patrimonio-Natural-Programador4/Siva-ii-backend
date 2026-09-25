# ------------------
# AgreementsDTO.py 
# ------------------------------------------------------------------------------------------------------------------- 

import decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict


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

    # Configuración compatible con Pydantic V2
    model_config = ConfigDict(from_attributes=True)
    
    