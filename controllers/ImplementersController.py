from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.ImplementersDto import ImplementerCreateBase
from services import ImplementersService

router = APIRouter(
    prefix='/implementadoras',
    tags=['Implementadoras']
)


@router.get('')
def listar_implementadoras(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return ImplementersService.listar_implementadoras(db)


@router.get('/{id_impl}')
def obtener_programa_por_id(id_impl: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    implementadoraa = ImplementersService.obtener_implementadora_por_id(id_impl, db)
    if not implementadoraa:
        raise HTTPException(status_code=404, detail='Implementadora no encontrado')
    return implementadoraa


@router.post('')
def crear_programa(payload: ImplementerCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = ImplementersService.crear_implementadora(payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response_request.dict(), status_code=status.HTTP_400_BAD_REQUEST)


@router.put('/{id_impl}')
def actualizar_programa(id_impl: int, payload: ImplementerCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = ImplementersService.actualizar_implementadora(id_impl, payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    status_code = status.HTTP_404_NOT_FOUND if response_request.mensaje == 'Implementadora no encontrado' else status.HTTP_400_BAD_REQUEST
    return JSONResponse(content=response_request.dict(), status_code=status_code)
