from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.GeneralCategoriesDTO import GeneralCategoriesBase, GeneralCategoriesCreateBase
from services import GeneralCategoriesService

router = APIRouter(
    prefix='/categoria-general',
    tags=['categoria-general']
)


@router.get('')
def list_general_categories(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return GeneralCategoriesService.list_general_categories(db)

    
@router.post('')
def create_general_categories(payload: GeneralCategoriesCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = GeneralCategoriesService.create_general_categories(payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response_request.dict(), status_code=status.HTTP_400_BAD_REQUEST)

