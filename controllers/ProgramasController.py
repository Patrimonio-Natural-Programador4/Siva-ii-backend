from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.ProgramsDTO import ProgramsCreateBase
from services import ProgramsService

router = APIRouter(
    prefix='/programas',
    tags=['Programas']
)


@router.get('')
def listar_programas(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return ProgramsService.listar_programas(db)


@router.get('/{id_programa}')
def obtener_programa_por_id(id_programa: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    programa = ProgramsService.obtener_programa_por_id(id_programa, db)
    if not programa:
        raise HTTPException(status_code=404, detail='Programa no encontrado')
    return programa


@router.post('')
def crear_programa(payload: ProgramsCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = ProgramsService.crear_programa(payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response_request.dict(), status_code=status.HTTP_400_BAD_REQUEST)


@router.put('/{id_programa}')
def actualizar_programa(id_programa: int, payload: ProgramsCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = ProgramsService.actualizar_programa(id_programa, payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    status_code = status.HTTP_404_NOT_FOUND if response_request.mensaje == 'Programa no encontrado' else status.HTTP_400_BAD_REQUEST
    return JSONResponse(content=response_request.dict(), status_code=status_code)
