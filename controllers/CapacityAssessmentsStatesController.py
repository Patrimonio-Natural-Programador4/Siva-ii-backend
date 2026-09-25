from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.CapacityAssessmentsStatesDTO import CapacityAssessmentsStatesCreateBase
from services import CapacityAssessmentsStatesService

router = APIRouter(
    prefix='/estados-capacidades',
    tags=['estados-capacidades']
)


@router.get('')
def listar_capacity_assessments_states(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return CapacityAssessmentsStatesService.listar_capacity_assessments_states(db)


@router.get('/{id}')
def obtener_capacity_assessments_states_por_id(id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    evaluacion = CapacityAssessmentsStatesService.obtener_capacity_assessments_states_por_id(id, db)
    if not evaluacion:
        raise HTTPException(status_code=404, detail='estado no encontrado')
    return evaluacion


@router.post('')
def crear_capacity_assessments_states(payload: CapacityAssessmentsStatesCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = CapacityAssessmentsStatesService.crear_capacity_assessments_states(payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response_request.dict(), status_code=status.HTTP_400_BAD_REQUEST)


@router.put('/{id}')
def actualizar_capacity_assessments_states(id: int, payload: CapacityAssessmentsStatesCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = CapacityAssessmentsStatesService.actualizar_capacity_assessments_states(id, payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    status_code = status.HTTP_404_NOT_FOUND if response_request.mensaje == 'Estado no encontrado' else status.HTTP_400_BAD_REQUEST
    return JSONResponse(content=response_request.dict(), status_code=status_code)
