from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
import logging
import json
from dto.ResponseRequest import ResponseRequest
from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.DocumentTypesDTO import DocumentypeCreateBase
from dto.Document_types_ECDTO import Document_types_EC
from services import Document_types_ECService

router = APIRouter(
    prefix="/tipo-documentos-evaluacion-capacidades",
    tags=["tipo-documentos-evaluacion-capacidades"],
)


@router.get(
    "", response_model=ResponseRequest
)  # user_oid: str = Depends(get_current_user_oid)
def list_document_types_ec(db: DbSession):
    try:
        # return
        result = Document_types_ECService.list_document_types_ec(db)
        data = json.loads(result.resultado) if result.resultado else {}
        return ResponseRequest(
            solicitud_exitosa=True,
            mensaje="{}".format(result.resultado),
            identity=data.get("id"),
        )
    except Exception as e:
        logging.error(f"Error listing Document_types_EC: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
