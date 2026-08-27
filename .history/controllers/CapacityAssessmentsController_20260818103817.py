from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.CapacityAssessmentsDTO import CapacityAssessmentsBase,CapacityAssessmentsCreate
from dto.ResponseRequest import ResponseRequest
from services import CapacityAssessments

router = APIRouter(
    prefix='/evaluaciones-de-capacidades',
    tags=['EvaluacionesDeCapacidades']
)


@router.get('')
def listar(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return CapacityAssessments.listar(db)

@router.get('/{id}')
def obtener_por_id(id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    pad = CapacityAssessments.obtener_por_id(id, db)
    if not pad:
        raise HTTPException(status_code=404, detail='evaluacion de capacidades  no encontrado')
    return pad


@router.post('', response_model=ResponseRequest)
def crear_programa(payload: CapacityAssessmentsCreate, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    try:
        
        print("  payload " , payload)
        response_request = CapacityAssessments.crear(payload, db, user_oid)

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