from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.KfwObservationsDTO import KfwObservationsBase, KfwObservationsCreateBase
from services import KfwObservationsService

router = APIRouter(
    prefix='/kfw',
    tags=['kfw']
)


@router.get('')
def list_kfw_observations(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return KfwObservationsService.list_kfw_observations(db)

    
@router.post('')
def create_kfw_observations(payload: KfwObservationsCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = KfwObservationsService.create_kfw_observations(payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response_request.dict(), status_code=status.HTTP_400_BAD_REQUEST)

