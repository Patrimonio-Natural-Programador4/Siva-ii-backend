# -------------------------------------------------------------------------------------------------------------------
# AgreementsControler.py Refactorizado cambiando logica, entregar al Service - 24 Septiembre 2026 15:26 hrs
# -------------------------------------------------------------------------------------------------------------------


from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query
from database.database import DbSession
from dto.AgreementsDTO import AgreementsListSP
from dto.ResponseRequest import ResponseRequest
from services.AgreementService import AgreementsService

# Inicialización del router de FastAPI
router = APIRouter(prefix='/agreements', tags=['Agreements'])

@router.get('', response_model=List[AgreementsListSP])
def listar_convenios(
    db: DbSession,
    p_agreement_id: Optional[int] = Query(None),
    p_type_ids: Optional[List[int]] = Query(None),
    p_modality_ids: Optional[List[int]] = Query(None),
    p_core_ids: Optional[List[int]] = Query(None),
    p_pillar_ids: Optional[List[int]] = Query(None),
    p_years: Optional[List[int]] = Query(None),
    p_phase: Optional[List[str]] = Query(None),
    p_stage_ids: Optional[List[int]] = Query(None),
    p_priority: Optional[List[str]] = Query(None),
    p_alert: Optional[List[str]] = Query(None),
    p_search: Optional[str] = Query(None),
    p_page: int = Query(1, ge=1),
    p_page_size: int = Query(25, ge=1),
):
    """
    Endpoint único para listar y filtrar convenios.
    Delega el procesamiento de la consulta al servicio 'AgreementService'.
    """
    try:
        resultado = AgreementService.listar_convenios(
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
        
               
        
