from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.ImplementersDto import ImplementerCreateBase
from services import PersonsService

router = APIRouter(
    prefix='/personas',
    tags=['Personas']
)


@router.get('')
def listar_implementadoras(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return PersonsService.listar(db)

"""
@router.post('')
def crear_programa(payload: ImplementerCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = PersonsService.(payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response_request.dict(), status_code=status.HTTP_400_BAD_REQUEST)
"""