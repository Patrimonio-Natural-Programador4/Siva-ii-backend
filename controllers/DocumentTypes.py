from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.DocumentTypesDTO import DocumentypeCreateBase
from services import DocumentTypesService

router = APIRouter(
    prefix='/tipo-documentos',
    tags=['TipoDocumentos']
)


@router.get('')
def listar_programas(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return DocumentTypesService.listar_tipos_documentos(db)


@router.get('/{id}')
def obtener_programa_por_id(id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    docu = DocumentTypesService.obtener_tipo_documento_por_id(id, db)
    if not programa:
        raise HTTPException(status_code=404, detail='Programa no encontrado')
    return programa


@router.post('')
def crear_programa(payload: DocumentypeCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = DocumentTypesService.crear_tipo_documento(payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response_request.dict(), status_code=status.HTTP_400_BAD_REQUEST)


@router.put('/{id_programa}')
def actualizar_programa(id_programa: int, payload: DocumentypeCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = DocumentTypesService.actualizar_tipo_documento(id_programa, payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    status_code = status.HTTP_404_NOT_FOUND if response_request.mensaje == 'Programa no encontrado' else status.HTTP_400_BAD_REQUEST
    return JSONResponse(content=response_request.dict(), status_code=status_code)
