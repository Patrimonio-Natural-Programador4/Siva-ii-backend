from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi import status
from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.AccionesSolicitudAprobacionDTO import AccionesSolicitudAprobacionBase
from dto.ResponseRequest import ResponseRequest
from dto.SolicitudAprobacionHistorialDTO import SolicitudAprobacionHistorialDTOBase
from dto.ViajesDTO import ViajesCreate
from services import ViajesService, SolicitudesAprobacionService

router = APIRouter(
    prefix='/viajes',
    tags=['Viajes']
)

@router.get("/listados")
def lista_generica(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return ViajesService.lista_generica(db, user_oid)

@router.get("/listados_viajes")
def lista_generica(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return ViajesService.lista_generica_lista_viajes(db)
    
@router.post("", response_model=ResponseRequest)
def crear_viaje(viaje: ViajesCreate, db: DbSession, background_tasks: BackgroundTasks, user_oid: str = Depends(get_current_user_oid)):
    try:

        response_request = ViajesService.crear_viaje(viaje, db, user_oid, background_tasks)
        
        if response_request.solicitud_exitosa:
            return JSONResponse(
                content=response_request.dict(),
                status_code=status.HTTP_201_CREATED
            )
        else:
            return JSONResponse(
                content=response_request.dict(),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        # return RolesService.crear_rol(rol, db)
    except HTTPException as e:
        print(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("")
def listar_viajes_filtro(
    db: DbSession,
    page: int = Query(...),
    filtro: str = Query(...),
    estado: list[int] = Query(...),
    fechaDesde: Optional[str] = Query(None),
    fechaHasta: Optional[str] = Query(None),
    programa: Optional[int] = Query(None),
    user_oid: str = Depends(get_current_user_oid)
):
   
    if fechaDesde == "null":
        fechaDesde = None

    if fechaHasta == "null":
        fechaHasta = None
    return ViajesService.listar_viajes_por_usuario_sp(db, user_oid, page, filtro, estado, fechaDesde, fechaHasta, programa)
    # return ViajesService.listar_viajes(db, decoded["oid"])


@router.get("/{guid}/detalle", response_model=ViajesCreate)
def obtener_viaje(guid: str, db: DbSession, user_oid: str = Depends(get_current_user_oid)) -> ViajesCreate:
    viaje = ViajesService.obtener_viaje_por_id(guid, db)
    if not viaje:
        raise HTTPException(status_code=404, detail="Viaje no encontrado")
    return viaje

@router.get("/{guid}/validar_acciones_aprobacion")
def validar_acciones_solicitud_aprobacion(guid: str, tipo: str, db: DbSession, user_oid: str = Depends(get_current_user_oid))-> list[SolicitudAprobacionHistorialDTOBase]:
    try:
        viaje = ViajesService.obtener_viaje_por_id(guid, db)
        id_categoria = SolicitudesAprobacionService.obtener_categoria_aprobacion(tipo, db)
        response_request = SolicitudesAprobacionService.validar_habilitar_acciones_solicitud_aprobacion(viaje.id_viaje, id_categoria, user_oid, db, viaje.guid_msft)


        # response_request = ViajesService.crear_viaje(viaje, db, decoded["oid"])
        
        # if response_request.solicitud_exitosa:
        return JSONResponse(
            content=response_request.dict(),
            status_code=status.HTTP_200_OK
        )
        # else:
        #     return JSONResponse(
        #         content=response_request.dict(),
        #         status_code=status.HTTP_200_OK
        #     )
        # return RolesService.crear_rol(rol, db)
    except HTTPException as e:
        print(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{guid}/accion_solicitud_aprobacion", response_model=ResponseRequest)
def accion_solicitud_aprobacion(
    guid: str,
    accion: AccionesSolicitudAprobacionBase,
    db: DbSession,
    user_oid: str = Depends(get_current_user_oid)
):
    try:
        viaje = ViajesService.obtener_viaje_por_id(guid, db)
        tipo_solicitud = accion.tipo_solicitud or ViajesService.CATEGORIA_APROBACION_SOLICITUD_VIAJE
        id_categoria = SolicitudesAprobacionService.obtener_categoria_aprobacion(tipo_solicitud, db)
        response_request = SolicitudesAprobacionService.ejecutar_accion_solicitud_aprobacion(
            viaje,
            accion,
            id_categoria,
            user_oid,
            db,
        )
        return JSONResponse(
            content=response_request.dict(),
            status_code=status.HTTP_200_OK if response_request.solicitud_exitosa else status.HTTP_400_BAD_REQUEST
        )
    except HTTPException as e:
        print(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

