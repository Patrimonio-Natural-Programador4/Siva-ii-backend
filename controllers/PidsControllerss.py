from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.ProgramsDTO import ProgramsCreateBase
from services import PidsServicee

router = APIRouter(
    prefix='/pids',
    tags=['Pids']
)


@router.get('')
def listar_programas(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return PidsServicee.listar(db)

