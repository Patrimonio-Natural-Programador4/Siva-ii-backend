from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.AgreementOriginsDTO import AgreementOriginsBase, AgreementOriginsCreateBase
from services import AgreementOriginsServicie

router = APIRouter(
    prefix='/acuerdos-origen',
    tags=['acuerdos-origen']
)


@router.get('')
def list_agreement_origins(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return AgreementOriginsServicie.list_agreement_origins(db)


@router.post('')
def create_agreement_origins(payload: AgreementOriginsCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = AgreementOriginsServicie.create_agreement_origins(payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response_request.dict(), status_code=status.HTTP_400_BAD_REQUEST)

