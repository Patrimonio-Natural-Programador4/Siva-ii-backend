from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.ProductsStateDTO import ProductsStateBase, ProductsStateCreateBase
from services import ProductsStateService

router = APIRouter(
    prefix='/estados-productos',
    tags=['estados-productos']
)


@router.get('')
def list_products_state(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return ProductsStateService.list_products_state(db)


@router.get('/{id}')
def get_disbursement_state_by_id(id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    state = ProductsStateService.get_products_state_by_id(id, db)
    if not state:
        raise HTTPException(status_code=404, detail='estado no encontrado')
    return state


@router.post('')
def create_disbursement_state(payload: ProductsStateCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = ProductsStateService.create_products_state(payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response_request.dict(), status_code=status.HTTP_400_BAD_REQUEST)


@router.put('/{id}')
def update_disbursement_state(id: int, payload: ProductsStateCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = ProductsStateService.update_products_state(id, payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    status_code = status.HTTP_404_NOT_FOUND if response_request.mensaje == 'Estado no encontrado' else status.HTTP_400_BAD_REQUEST
    return JSONResponse(content=response_request.dict(), status_code=status_code)
