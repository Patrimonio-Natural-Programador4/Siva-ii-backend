from fastapi import APIRouter, Depends, HTTPException,Query
from fastapi.responses import JSONResponse
from fastapi import status
from typing import Optional

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.CapacityAssessmentsDTO import CapacityAssessmentsBase,CapacityAssessmentsCreate
from dto.ResponseRequest import ResponseRequest
from services import CapacityAssessments
from services import SolicitudesAprobacionService
from dto.CapacityAssessmentsDTO import CapacityAssessmentListSP
from dto.AccionesSolicitudAprobacionCapacidadDTO import AccionSolicitudAprobacionCapacidad
from dto.AccionesSolicitudAprobacionDTO import AccionSolicitudAprobacion

CATEGORIA_APROBACION = "APP_EC"


router = APIRouter(
    prefix='/evaluaciones-de-capacidades',
    tags=['EvaluacionesDeCapacidades']
)


@router.get('')
def listar(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return CapacityAssessments.listar(db)

@router.get("/filtro")
def listar_capacity_assessments_filtro(
    db: DbSession,
    user_oid: str = Depends(get_current_user_oid),
    page: int = Query(...),
    estado: list[int] = Query([-1]),
    programa: Optional[int] = Query(-1),
    filtro: str = Query(""),
):
    try:
        return CapacityAssessments.listar_capacity_assessments_por_usuario_sp(
            db, user_oid, page, estado, filtro, programa
        )
        #return "me ve"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
     
  
@router.get("/filtro-test")
def listar_capacity_assessments_filtro_test(
    db: DbSession,
    guid: str = Depends(get_current_user_oid),
    page: int = Query(...),
    estado: list[int] = Query([-1]),
    programa: Optional[int] = Query(-1),
    filtro: str = Query(""),
):
    try:
        return CapacityAssessments.listar_capacity_assessments_por_usuario_sp(
            db, guid, page, estado, filtro, programa
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/{id}')
def obtener_por_id(id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    pad = CapacityAssessments.obtener_por_id(id, db)
    if not pad:
        raise HTTPException(status_code=404, detail='evaluacion de capacidades  no encontrado')
    return pad


@router.post('', response_model=ResponseRequest)
def crear_programa(payload: CapacityAssessmentsCreate, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    try:      
        response_request = CapacityAssessments.crear(payload, db, user_oid)
        if response_request.solicitud_exitosa:
            return JSONResponse(
                content=response_request.model_dump(),
                status_code=status.HTTP_201_CREATED
            )
        if response_request.solicitud_exitosa==False:
                   return JSONResponse(
                       content=response_request.model_dump(),
                       status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
                   )       
    except HTTPException as e:
        print(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put('/{guid}', response_model=ResponseRequest)
def actualizar(guid: str, payload: CapacityAssessmentsCreate, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    try:
        evaluacion_db = CapacityAssessments.obtener_por_guid(guid, db)
        if not evaluacion_db:
            raise HTTPException(status_code=404, detail='Evaluación de capacidades no encontrada')
        response_request = CapacityAssessments.actualizar(evaluacion_db.id, payload, db)
        return JSONResponse(
            content=response_request.dict(),
            status_code=status.HTTP_200_OK if response_request.solicitud_exitosa else status.HTTP_400_BAD_REQUEST
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))   

@router.get('/{guid}/detalle')
def obtener_por_guid(guid: str, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    evaluacion = CapacityAssessments.obtener_por_guid(guid, db)
    if not evaluacion:
        raise HTTPException(status_code=404, detail='Evaluación de capacidades no encontrada')
    return evaluacion


@router.get('/{guid}/validar_acciones_aprobacion')
def validar_acciones_solicitud_aprobacion(guid: str, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    try:
        evaluacion = CapacityAssessments.obtener_por_guid(guid, db)
        if not evaluacion:
            raise HTTPException(status_code=404, detail='Evaluación de capacidades no encontrada')
        id_categoria = SolicitudesAprobacionService.obtener_categoria_aprobacion(CATEGORIA_APROBACION, db)
        respuesta = SolicitudesAprobacionService.validar_habilitar_acciones_solicitud_aprobacion(
            evaluacion.id, id_categoria, user_oid, db
        )
        return JSONResponse(content=respuesta.dict(), status_code=status.HTTP_200_OK)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





@router.post('/{guid}/accion_solicitud_aprobacion', response_model=ResponseRequest)
def accion_solicitud_aprobacion(
    guid: str,
    accion: AccionSolicitudAprobacionCapacidad,
    db: DbSession,
    user_oid: str = Depends(get_current_user_oid),
    
):
  
    try:
        
        evaluacion_db = CapacityAssessments.obtener_por_guid(guid, db)
        if not evaluacion_db:
            raise HTTPException(
                status_code=404,
                detail='Evaluación de capacidades no encontrada',
            )

        accion.id_evaluacion = evaluacion_db.id
        accion.id_solicitud_aprobacion = evaluacion_db.approval_request_id
        id_categoria = (
            SolicitudesAprobacionService.obtener_categoria_aprobacion(
                CATEGORIA_APROBACION, db
            )
        )

        respuesta = CapacityAssessments.procesar_accion_solicitud_aprobacion(
            accion, user_oid, id_categoria, db
        )

        return JSONResponse(
            content=respuesta.dict(),
            status_code=(
                status.HTTP_200_OK
                if respuesta.solicitud_exitosa
                else status.HTTP_400_BAD_REQUEST
            ),
        )
       
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))