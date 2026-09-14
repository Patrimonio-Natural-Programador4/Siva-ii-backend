#CONTROLLER ESTUDIOS PREVIOS
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi import status
from dto.ResponseRequest import ResponseRequest
from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid

from dto.AccionesSolicitudAprobacionDTO import AccionSolicitudAprobacion
from services import PreviousStudiesService, SolicitudesAprobacionService
from repository import PreviousStudiesRepository
from dto.PreviousStudiesDTO import PreviousStudiesCreate
from services import PreviousStudiesService
CATEGORIA_APROBACION = "APP_EP"

router = APIRouter(
    prefix='/estudios-previos',
    tags=['EstudiosPrevios']
)


@router.get('')
def listar(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return PreviousStudiesService.listar(db)


@router.get("/filtro")
def listar_previous_studies_filtro(
    db: DbSession,
    user_oid: str = Depends(get_current_user_oid),
    page: int = Query(...),
    estado: list[int] = Query([-1]),
    programa: Optional[int] = Query(-1),
    filtro: str = Query(""),
):
    try:
        return PreviousStudiesService.listar_previous_studies_por_usuario_sp(
            db, user_oid, page, estado, filtro, programa
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get('/{id}')
def obtener_estudio_por_id(id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    estudio = PreviousStudiesService.obtener_est_previo_por_id(id, db)
    if not estudio:
        raise HTTPException(status_code=404, detail='Estudio previo no encontrado')
    return estudio

@router.post('', response_model=ResponseRequest)
def crear_estudio(payload: PreviousStudiesCreate, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    try:
        response_request = PreviousStudiesService.crearEstudioPrevio(payload, db, user_oid)

        if response_request.solicitud_exitosa:
            return JSONResponse(
                content=response_request.model_dump(),
                status_code=status.HTTP_201_CREATED
            )
        else:
            return JSONResponse(
                content=response_request.model_dump(),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    except HTTPException as e:
        print(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))  
    
@router.get('/{guid}/detalle')
def obtener_por_guid(guid: str, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    estudio = PreviousStudiesService.obtener_por_guid(guid, db)
    if not estudio:
        raise HTTPException(status_code=404, detail='Estudio previo no encontrado')
    return estudio


@router.get('/{guid}/validar_acciones_aprobacion')
def validar_acciones_solicitud_aprobacion(guid: str, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    try:
        estudio = PreviousStudiesService.obtener_por_guid(guid, db)
        if not estudio:
            raise HTTPException(status_code=404, detail='Estudio previo no encontrado')
        id_categoria = SolicitudesAprobacionService.obtener_categoria_aprobacion(CATEGORIA_APROBACION, db)
        respuesta = SolicitudesAprobacionService.validar_habilitar_acciones_solicitud_aprobacion(
            estudio.id, id_categoria, user_oid, db
        )
        return JSONResponse(content=respuesta.model_dump(), status_code=status.HTTP_200_OK)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/{guid}/accion_solicitud_aprobacion', response_model=ResponseRequest)
def accion_solicitud_aprobacion(
    guid: str,
    accion: AccionSolicitudAprobacion,
    db: DbSession,
    user_oid: str = Depends(get_current_user_oid),
):
    try:
        estudio_db = PreviousStudiesRepository.obtener_por_guid(guid, db)
        if not estudio_db:
            raise HTTPException(status_code=404, detail='Estudio previo no encontrado')

        if accion.estudio_previo is None:
            accion.estudio_previo = PreviousStudiesCreate()

        accion.estudio_previo.id = estudio_db.id
        accion.estudio_previo.guid = estudio_db.guid
        accion.id_solicitud_aprobacion = estudio_db.approval_request_id

        id_categoria = SolicitudesAprobacionService.obtener_categoria_aprobacion(CATEGORIA_APROBACION, db)
        respuesta = PreviousStudiesService.procesar_accion_solicitud_aprobacion(
            accion, user_oid, id_categoria, db
        )
        return JSONResponse(
            content=respuesta.model_dump(),
            status_code=status.HTTP_200_OK if respuesta.solicitud_exitosa else status.HTTP_400_BAD_REQUEST,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.put('/{guid}', response_model=ResponseRequest)
def actualizar_estudio(guid: str, payload: PreviousStudiesCreate, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    try:
        estudio_db = PreviousStudiesRepository.obtener_por_guid(guid, db)
        if not estudio_db:
            raise HTTPException(status_code=404, detail='Estudio previo no encontrado')
        response_request = PreviousStudiesService.actualizar(estudio_db.id, payload, db)
        return JSONResponse(
            content=response_request.model_dump(),
            status_code=status.HTTP_200_OK if response_request.solicitud_exitosa else status.HTTP_400_BAD_REQUEST
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))