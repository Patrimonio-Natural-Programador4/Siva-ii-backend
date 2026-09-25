       
        
# --------------------------------------------CORRECCION SIMPLIFICADA - INICIO - 001 ------------------------------------------------

# ***************************************
# AgreementsController.py -- 
# ***************************************

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from database.database import DbSession
from dto.AgreementsDTO import AgreementsListSP
from dto.ResponseRequest import ResponseRequest
from repository import AgreementsRepository

# Inicialización del router de FastAPI
router = APIRouter(prefix='/agreements', tags=['Agreements'])


@router.get('', response_model=ResponseRequest)
def listar_convenios(
    db: DbSession,# CORREGIDO: Se colocó primero y sin "= Depends()"
    p_agreement_id: Optional[int] = Query(None),
    p_type_ids: Optional[list[int]] = Query(None),
    p_modality_ids: Optional[list[int]] = Query(None),
    p_core_ids: Optional[list[int]] = Query(None),
    p_pillar_ids: Optional[list[int]] = Query(None),
    p_years: Optional[list[int]] = Query(None),
    p_phase: Optional[list[str]] = Query(None),
    p_stage_ids: Optional[list[int]] = Query(None),
    p_priority: Optional[list[str]] = Query(None),
    p_alert: Optional[list[str]] = Query(None),
    p_search: Optional[str] = Query(None),
    p_page: int = Query(1, ge=1),
    p_page_size: int = Query(25, ge=1),
    
):
    """
    Endpoint único para listar y filtrar convenios. Executa la función 'public.list_agreements'
    en la base de datos a través de 'AgreementsRepository'.
    """
    try:
        resultado = AgreementsRepository.listar_convenios_sp(
            db=db,
            p_agreement_id=p_agreement_id,
            p_type_ids=p_type_ids,
            p_modality_ids=p_modality_ids,
            p_core_ids=p_core_ids,
            p_pillar_ids=p_pillar_ids,
            p_years=p_years,
            p_phase=p_phase,
            p_stage_ids=p_stage_ids,
            p_priority=p_priority,
            p_alert=p_alert,
            p_search=p_search,
            p_page=p_page,
            p_page_size=p_page_size
        )
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# -------------------------------------------------------------------------------------------------------------------