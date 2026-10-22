from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from services import PillarsServices

router = APIRouter(
    prefix='/pilares',
    tags=['Pilares']
)


@router.get('')
def listar_pilares(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    print("pilares")
    return PillarsServices.listar(db)

