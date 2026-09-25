from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.ImplementerTypesDTO import Implementer_typesBase,Implementer_typesCreateBase,Implementer_typesUpdateBase
from services import Implementer_typesService

router = APIRouter(
    prefix='/tipos-implementadoras',
    tags=['tipos-implementadoras']
)


@router.get('')
def listar_tipos_implementadoras(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return Implementer_typesService.listar_tipos_implementadora(db)


@router.get('/{id}')
def obtener_tipos_implementadoras_por_id(id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    tipos_implementadora = Implementer_typesService.obtener_tipos_implementadora_por_id(id, db)
    if not tipos_implementadora:
        raise HTTPException(status_code=404, detail='Tipo implementadora no encontrado')
    return tipos_implementadora


@router.post('')
def crear_tipos_implementadoras(payload: Implementer_typesCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = Implementer_typesService.crear_tipos_implementadora(payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.model_dump(), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response_request.model_dump(), status_code=status.HTTP_400_BAD_REQUEST)


@router.put('/{id}')
def actualizar_tipos_implementadoras(id: int, payload: Implementer_typesCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = Implementer_typesService.actualizar_tipos_implementadora(id, payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.model_dump(), status_code=status.HTTP_200_OK)

    status_code = status.HTTP_404_NOT_FOUND if response_request.mensaje == 'Tipo implementadora no encontrada' else status.HTTP_400_BAD_REQUEST
    return JSONResponse(content=response_request.model_dump(), status_code=status_code)
