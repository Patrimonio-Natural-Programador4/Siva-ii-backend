from typing import Optional, List
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, Query,Depends
from database.database import DbSession
from dto.AgreementsDTO import AgreementsListSP
from dto.ResponseRequest import ResponseRequest
from services.AgreementService import AgreementsService
#from services import AgreementssService
from fastapi import status
from services import AgreementssService
from dto.agreementDTO import AgreementsBase,AgreementsCreateBase
from dependencies.auth_dependency import get_current_user_oid

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
    try:
        resultado = AgreementsService.listar_convenios(
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
    
"""
@router.get('/listar')
def listar( db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    acuerdos = AgreementssService.listar( db)
    if not acuerdos:
        raise HTTPException(status_code=404, detail='Error al listar acuerdos')
    return acuerdos
"""

@router.get('/{id}')
def listar(id, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    acuerdo = AgreementssService.obtener_por_id( id,db)
    if not acuerdo:
        raise HTTPException(status_code=404, detail='Error al obtener acuerdo por id')
    return acuerdo


from fastapi.encoders import jsonable_encoder

@router.post("/")
def crear_agreement(payload: AgreementsCreateBase, db: DbSession,
                    user_oid: str = Depends(get_current_user_oid)):
    response_request = AgreementssService.crear_agreement(payload, db)
    status_code = status.HTTP_201_CREATED if response_request.solicitud_exitosa else status.HTTP_400_BAD_REQUEST
    return JSONResponse(content=jsonable_encoder(response_request.model_dump()), status_code=status_code)