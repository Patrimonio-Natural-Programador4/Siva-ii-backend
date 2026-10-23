from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.RisksDTO import RisksCreateBase
from services import RisksService

router = APIRouter(
    prefix='/riesgos',
    tags=['riesgos']
)


@router.get('')
def list_risk(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return RisksService.list_risks(db)


@router.get('/{id_risk}')
def get_risk_by_id(id_risk: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    risk = RisksService.get_risk_by_id(id_risk, db)
    if not risk:
        raise HTTPException(status_code=404, detail='Riesgo no encontrado')
    return risk


@router.post('')
def create_risk(payload: RisksCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = RisksService.create_risk(payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response_request.dict(), status_code=status.HTTP_400_BAD_REQUEST)


@router.put('/{id_risk}')
def update_risk(id_risk: int, payload: RisksCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = RisksService.update_risk(id_risk, payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    status_code = status.HTTP_404_NOT_FOUND if response_request.mensaje == 'Riesgo no encontrado' else status.HTTP_400_BAD_REQUEST
    return JSONResponse(content=response_request.dict(), status_code=status_code)

@router.get('/estudio-previo/{id_previous_study}')
def list_risks_by_previous_studies(
    id_previous_study: int,
    db: DbSession,
    user_oid = Depends(get_current_user_oid)
):
    return RisksService.list_risk_by_previous_study(id_previous_study, db)

