from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.PadStatusDTO import PadStatusCreateBase, PadStatusBase
from services import PadStatusService

router = APIRouter(
    prefix='/estados',
    tags=['estados']
)


@router.get('')
def list_pad_status(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return PadStatusService.list_pad_status(db)

    
@router.post('')
def create_pad_status(payload: PadStatusCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = PadStatusService.create_pad_status(payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response_request.dict(), status_code=status.HTTP_400_BAD_REQUEST)

