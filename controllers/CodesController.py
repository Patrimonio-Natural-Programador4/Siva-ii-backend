from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.CodesDTO import CodesBase, CodesCreateBase
from services import CodesService

router = APIRouter(
    prefix='/codigos',
    tags=['codigos']
)


@router.get('')
def list_codes(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return CodesService.list_codes(db)

    
@router.post('')
def create_code(payload: CodesCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = CodesService.create_codes(payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response_request.dict(), status_code=status.HTTP_400_BAD_REQUEST)

