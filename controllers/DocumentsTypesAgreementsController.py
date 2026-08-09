from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.DocumentsTypesAgreements import DocumentsTypesAgreementsBase
from services import DocumentsTypesAgreementsSevice

router = APIRouter(
    prefix='/tipos-documentos-acuerdos',
    tags=['tipos-documentos-acuerdos']
)


@router.get('')
def listar_tipo_documentos_acuerdos(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return DocumentsTypesAgreementsSevice.listar(db)