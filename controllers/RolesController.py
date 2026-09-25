from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.RolesDTO import RolesCreateBase
from services import RolesService

router = APIRouter(
    prefix='/roles',
    tags=['Roles']
)


@router.get('')
def listar_roles(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return RolesService.listar_roles(db)


@router.get('/listados')
def listar_modulos(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return RolesService.listar_modulos(db)


@router.get('/controles-modulos')
def listar_controles_por_modulo(db: DbSession, ids: str = '', user_oid: str = Depends(get_current_user_oid)):
    try:
        ids_modulos = [int(item.strip()) for item in ids.split(',') if item.strip()] if ids else []
        return RolesService.listar_controles_por_modulo(ids_modulos, db)
    except ValueError:
        raise HTTPException(status_code=400, detail='Parametro ids invalido')


@router.get('/{id_rol}')
def obtener_rol_por_id(id_rol: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    rol = RolesService.obtener_rol_por_id(id_rol, db)
    if not rol:
        raise HTTPException(status_code=404, detail='Rol no encontrado')
    return rol


@router.post('')
def crear_rol(payload: RolesCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = RolesService.crear_rol(payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response_request.dict(), status_code=status.HTTP_400_BAD_REQUEST)


@router.put('/{id_rol}')
def actualizar_rol(id_rol: int, payload: RolesCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = RolesService.actualizar_rol(id_rol, payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    status_code = status.HTTP_404_NOT_FOUND if response_request.mensaje == 'Rol no encontrado' else status.HTTP_400_BAD_REQUEST
    return JSONResponse(content=response_request.dict(), status_code=status_code)
