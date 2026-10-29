from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.AgreementsProductsDTO import AgreementsProductsCreateBase
from services import AgreementsProductsService

router = APIRouter(
    prefix='/acuerdos-productos',
    tags=['acuerdos-productos']
)


@router.get('')
def list_agreements_products(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return AgreementsProductsService.list_agreements_products(db)


@router.get('/acuerdo/{agreement_id}')
def list_agreements_products_by_agreement(agreement_id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return AgreementsProductsService.list_agreements_products_by_agreement(agreement_id, db)

@router.get('/estudio-previo/{previous_studies_id}')
def list_agreements_products_by_previous_studies(previous_studies_id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return AgreementsProductsService.list_agreements_products_by_previous_studies(previous_studies_id, db)


@router.get('/{id}')
def get_agreements_products_by_id(id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    agreements_products = AgreementsProductsService.get_agreements_products_by_id(id, db)
    if not agreements_products:
        raise HTTPException(status_code=404, detail='Producto no encontrado')
    return agreements_products


@router.post('')
def create_agreements_products(payload: AgreementsProductsCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = AgreementsProductsService.create_agreements_products(payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=jsonable_encoder(response_request), status_code=status.HTTP_200_OK)

    return JSONResponse(content=jsonable_encoder(response_request), status_code=status.HTTP_400_BAD_REQUEST)


@router.put('/{id}')
def update_agreements_products(id: int, payload: AgreementsProductsCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = AgreementsProductsService.update_agreements_products(id, payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=jsonable_encoder(response_request), status_code=status.HTTP_200_OK)

    status_code = status.HTTP_404_NOT_FOUND if response_request.mensaje == 'Producto no encontrado' else status.HTTP_400_BAD_REQUEST
    return JSONResponse(content=jsonable_encoder(response_request), status_code=status_code)



@router.get('/estudio-previo/{previous_studies_id}/arbol')
def get_tree_by_previous_studies(previous_studies_id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return AgreementsProductsService.get_tree_by_previous_studies(previous_studies_id, db)