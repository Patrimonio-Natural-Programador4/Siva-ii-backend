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


# crear tipo docu
@router.post('')
def crear_tipo_doc(payload: DocumentsTypesAgreementsBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = DocumentsTypesAgreementsSevice.crear_tipo_doc(payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.model_dump(), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response_request.model_dump(), status_code=status.HTTP_400_BAD_REQUEST)


# editar tipo docu
@router.put("/{id}")
def editar_tipo_doc_acu(
    id: int, 
    payload: DocumentsTypesAgreementsBase, 
    db: DbSession, 
    user_oid: str = Depends(get_current_user_oid)
):
    response_request = DocumentsTypesAgreementsSevice.editar_tipo_doc_acu(id, payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.model_dump(), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response_request.model_dump(), status_code=status.HTTP_400_BAD_REQUEST)


@router.get('/{id}')
def obtener_tipo_doc_acu_por_id(id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    doc = DocumentsTypesAgreementsSevice.obtener_tipo_doc_acu_por_id(id, db)
    if not doc:
        raise HTTPException(status_code=404, detail='Tipo documento no encontrado')
    return doc
