from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.ActivitiesDTO import ActivitiesListDTO
from services import ActivitiesService

router = APIRouter(
    prefix='/actividades',
    tags=['actividades']
)


@router.get('')
def listar_activities(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return ActivitiesService.Activities_list(db)

