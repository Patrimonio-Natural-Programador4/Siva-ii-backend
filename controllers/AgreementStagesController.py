from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.agreementStagesDTO import AgreementStagesBase,AgreementStagesCreateBase
from services import AgreementStagesService

router = APIRouter(
    prefix='/fases-del-acuerdo',
    tags=['fases-del-acuerdo']
)


@router.get('')
def get_agrement_stages(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return AgreementStagesService.listar(db)


@router.get('/{id}')
def obtener_fases_acuerdo_por_id(id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    fase_acuerdo = AgreementStagesService.obtener_pad_por_id(id, db)
    if not fase_acuerdo:
        raise HTTPException(status_code=404, detail='Fase del acuerdo no encontrado')
    return fase_acuerdo