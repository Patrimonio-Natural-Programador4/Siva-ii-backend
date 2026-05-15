from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.FlujosAprobacionDTO import DelegacionRolesUsuariosBase, FlujosAprobacionBase, RolesAprobacionBase
from services import FlujosAprobacionService


router = APIRouter(
    prefix='/flujos-aprobacion',
    tags=['FlujosAprobacion']
)


@router.get('/roles')
def listar_roles_aprobacion(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return FlujosAprobacionService.listar_roles_aprobacion(db)


@router.get('/roles/listados')
def listar_roles_aprobacion_listados(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return FlujosAprobacionService.listar_roles_aprobacion_listados(db)


@router.get('/roles/{id_rol_aprobacion}')
def obtener_rol_aprobacion(id_rol_aprobacion: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    role = FlujosAprobacionService.obtener_rol_aprobacion_por_id(id_rol_aprobacion, db)
    if not role:
        raise HTTPException(status_code=404, detail='Rol de aprobación no encontrado')
    return role


@router.post('/roles')
def crear_rol_aprobacion(payload: RolesAprobacionBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response = FlujosAprobacionService.crear_rol_aprobacion(payload, db)
    status_code = status.HTTP_200_OK if response.solicitud_exitosa else status.HTTP_400_BAD_REQUEST
    return JSONResponse(content=response.dict(), status_code=status_code)


@router.put('/roles/{id_rol_aprobacion}')
def actualizar_rol_aprobacion(id_rol_aprobacion: int, payload: RolesAprobacionBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response = FlujosAprobacionService.actualizar_rol_aprobacion(id_rol_aprobacion, payload, db)
    status_code = status.HTTP_200_OK if response.solicitud_exitosa else status.HTTP_400_BAD_REQUEST
    if response.mensaje == 'Rol de aprobación no encontrado':
        status_code = status.HTTP_404_NOT_FOUND
    return JSONResponse(content=response.dict(), status_code=status_code)


@router.get('')
def listar_flujos_aprobacion(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return FlujosAprobacionService.listar_flujos_aprobacion(db)


@router.get('/listados')
def listar_flujos_aprobacion_listados(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return FlujosAprobacionService.listar_flujos_aprobacion_listados(db)


@router.get('/{id_flujo_aprobacion}')
def obtener_flujo_aprobacion(id_flujo_aprobacion: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    flow = FlujosAprobacionService.obtener_flujo_aprobacion_por_id(id_flujo_aprobacion, db)
    if not flow:
        raise HTTPException(status_code=404, detail='Flujo no encontrado')
    return flow


@router.post('')
def crear_flujo_aprobacion(payload: FlujosAprobacionBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response = FlujosAprobacionService.crear_flujo_aprobacion(payload, db)
    status_code = status.HTTP_201_CREATED if response.solicitud_exitosa else status.HTTP_400_BAD_REQUEST
    return JSONResponse(content=response.dict(), status_code=status_code)


@router.put('/{id_flujo_aprobacion}')
def actualizar_flujo_aprobacion(id_flujo_aprobacion: int, payload: FlujosAprobacionBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response = FlujosAprobacionService.actualizar_flujo_aprobacion(id_flujo_aprobacion, payload, db)
    status_code = status.HTTP_200_OK if response.solicitud_exitosa else status.HTTP_400_BAD_REQUEST
    if response.mensaje == 'Flujo no encontrado':
        status_code = status.HTTP_404_NOT_FOUND
    return JSONResponse(content=response.dict(), status_code=status_code)


# @router.get('/delegaciones')
# def listar_delegaciones_roles_usuarios(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
#     return FlujosAprobacionService.listar_delegaciones_roles_usuarios(db)


# @router.get('/delegaciones/listados/{id_delegacion}')
# def listar_delegaciones_listados(id_delegacion: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
#     return FlujosAprobacionService.listar_delegaciones_listados(id_delegacion, db)


# @router.get('/delegaciones/{id_delegacion}')
# def obtener_delegacion_roles_usuarios(id_delegacion: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
#     delegation = FlujosAprobacionService.obtener_delegacion_roles_usuarios_por_id(id_delegacion, db)
#     if not delegation:
#         raise HTTPException(status_code=404, detail='Delegación no encontrada')
#     return delegation


# @router.post('/delegaciones')
# def crear_delegacion_roles_usuarios(payload: DelegacionRolesUsuariosBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
#     response = FlujosAprobacionService.crear_delegacion_roles_usuarios(payload, db)
#     status_code = status.HTTP_200_OK if response.solicitud_exitosa else status.HTTP_400_BAD_REQUEST
#     return JSONResponse(content=response.dict(), status_code=status_code)


# @router.put('/delegaciones')
# def actualizar_delegacion_roles_usuarios(payload: DelegacionRolesUsuariosBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
#     response = FlujosAprobacionService.actualizar_delegacion_roles_usuarios(payload, db)
#     status_code = status.HTTP_200_OK if response.solicitud_exitosa else status.HTTP_400_BAD_REQUEST
#     if response.mensaje == 'Delegación no encontrada':
#         status_code = status.HTTP_404_NOT_FOUND
#     return JSONResponse(content=response.dict(), status_code=status_code)