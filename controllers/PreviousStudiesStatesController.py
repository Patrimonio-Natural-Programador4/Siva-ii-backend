from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.PreviousStudiesStatesDTO import PreviousStudiesStatesCreateBase,PreviousStudiesStatesBase
from services import PreviousStudiesStatesService

router = APIRouter(
    prefix='/estados-estudios_previos',
    tags=['estados-estudios-previos']
)


@router.get('')
def listar_estudios_previos_estado(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return PreviousStudiesStatesService.listar_estudios_previos_estado(db)


@router.get('/{id}')
def obtener_estudios_previos_estado_por_id(id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    estudio = PreviousStudiesStatesService.obtener_estudios_previos_estado_por_id(id, db)
    if not estudio:
        raise HTTPException(status_code=404, detail='estado no encontrado')
    return estudio


@router.post('')
def crear_estudios_previos_estado(payload: PreviousStudiesStatesCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = PreviousStudiesStatesService.crear_estudios_previos_estado(payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response_request.dict(), status_code=status.HTTP_400_BAD_REQUEST)


@router.put('/{id}')
def actualizar_estudios_previos_estado(id: int, payload: PreviousStudiesStatesCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = PreviousStudiesStatesService.actualizar_estudios_previos_estado(id, payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    status_code = status.HTTP_404_NOT_FOUND if response_request.mensaje == 'Estado no encontrado' else status.HTTP_400_BAD_REQUEST
    return JSONResponse(content=response_request.dict(), status_code=status_code)
