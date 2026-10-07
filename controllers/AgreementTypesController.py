from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.AgreementTypesDTO import AgreementTypesBase, AgreementTypesCreateBase
from services import AgreementTypesService

router = APIRouter(
    prefix='/tipos-acuerdos',
    tags=['tipos-acuerdos']
)


@router.get('')
def list_agreement_types(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return AgreementTypesService.list_agreement_types(db)

    
@router.post('')
def create_agreement_types(payload: AgreementTypesCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = AgreementTypesService.create_agreement_types(payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response_request.dict(), status_code=status.HTTP_400_BAD_REQUEST)

