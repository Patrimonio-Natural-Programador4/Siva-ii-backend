from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from services import DocumentsApprovalService
from dto.DocumentsApprovalDTO import DocumentsCreateBase
from dto.DocumentsApprovalDTO import DocumentsUpdateBase


router = APIRouter(prefix="/aprobacion-documentos", tags=["Aprobacion-documentos"])


@router.get("")
def listar_documentos(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return DocumentsApprovalService.listar_documentos_aprobados(db)


# crear docs
@router.post('')
def crear_documento(payload: DocumentsCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = DocumentsApprovalService.crear_documento(payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.model_dump(), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response_request.model_dump(), status_code=status.HTTP_400_BAD_REQUEST)



@router.get('/{id}')
def obtener_doc_por_id(id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    doc = DocumentsApprovalService.obtener_doc_por_id(
        id, 
        db)
    if not doc:
        raise HTTPException(status_code=404, detail='Documento no encontrado')
    return doc

# editar docs
@router.put("/{id}")
def editar_documento(
    id: int, 
    payload: DocumentsUpdateBase, 
    db: DbSession, 
    user_oid: str = Depends(get_current_user_oid)
):
    response_request = DocumentsApprovalService.editar_documento(id, payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.model_dump(), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response_request.model_dump(), status_code=status.HTTP_400_BAD_REQUEST)

