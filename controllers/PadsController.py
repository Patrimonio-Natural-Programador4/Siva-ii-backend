from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.PadsDTO import PadsCreateBase
from services import PadsService

router = APIRouter(
    prefix='/pads',
    tags=['pads']
)


@router.get('')
def listar_pads(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return PadsService.listar_pads(db)


@router.get('/{id}')
def obtener_pad_por_id(id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    pad = PadsService.obtener_pad_por_id(id, db)
    if not pad:
        raise HTTPException(status_code=404, detail='pad no encontrado')
    return pad


@router.post('')
def crear_pad(payload: PadsCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = PadsService.crear_pad(payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.model_dump(), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response_request.model_dump(), status_code=status.HTTP_400_BAD_REQUEST)


@router.put('/{id}')
def actualizar_pad(id: int, payload: PadsCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = PadsService.actualizar_pad(id, payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.model_dump(), status_code=status.HTTP_200_OK)

    status_code = status.HTTP_404_NOT_FOUND if response_request.mensaje == 'pad no encontrado' else status.HTTP_400_BAD_REQUEST
    return JSONResponse(content=response_request.model_dump(), status_code=status_code)
