from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.DisbursementDTO import DisbursementCreateBase
from services import DisbursementService

router = APIRouter(
    prefix='/desembolsos',
    tags=['desembolsos']
)


@router.get('')
def list_disbursement(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return DisbursementService.list_disbursement(db)


@router.get('/acuerdo/{agreement_id}')
def list_disbursement_by_agreement(agreement_id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return DisbursementService.list_disbursement_by_agreement(agreement_id, db)

@router.get('/estudio-previo/{previous_studies_id}')
def list_disbursement_by_previous_studies(previous_studies_id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return DisbursementService.list_disbursement_by_previous_studies(previous_studies_id, db)


@router.get('/{id}')
def get_disbursement_by_id(id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    disbursement = DisbursementService.get_disbursement_by_id(id, db)
    if not disbursement:
        raise HTTPException(status_code=404, detail='Desembolso no encontrado')
    return disbursement


@router.post('')
def create_disbursement(payload: DisbursementCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = DisbursementService.create_disbursement(payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=jsonable_encoder(response_request), status_code=status.HTTP_200_OK)

    return JSONResponse(content=jsonable_encoder(response_request), status_code=status.HTTP_400_BAD_REQUEST)


@router.put('/{id}')
def update_disbursement(id: int, payload: DisbursementCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = DisbursementService.update_disbursement(id, payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=jsonable_encoder(response_request), status_code=status.HTTP_200_OK)

    status_code = status.HTTP_404_NOT_FOUND if response_request.mensaje == 'Desembolso no encontrado' else status.HTTP_400_BAD_REQUEST
    return JSONResponse(content=jsonable_encoder(response_request), status_code=status_code)