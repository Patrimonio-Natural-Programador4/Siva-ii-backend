#CONTROLLER ESTUDIOS PREVIOS
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from dto.ResponseRequest import ResponseRequest
from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid

from dto.PreviousStudiesDTO import PreviousStudiesCreate
from services import PreviousStudiesService


router = APIRouter(
    prefix='/estudios-previos',
    tags=['EstudiosPrevios']
)


@router.get('')
def listar(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return PreviousStudiesService.listar(db)

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