from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.modalitiesDTO import modalitiesCreateBase
from services import ModalitiesService

router = APIRouter(
    prefix='/modalidades',
    tags=['Modalidades']
)


@router.get('')
def listar_modalidades(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return ModalitiesService.listar_modalidades(db)


@router.post('')
def crear_modalidad(payload: modalitiesCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = ModalitiesService.crear_modalidad(payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response_request.dict(), status_code=status.HTTP_400_BAD_REQUEST)

