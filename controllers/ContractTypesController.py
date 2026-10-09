from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.ContractTypesDTO import ContractTypesBase, ContractTypesCreateBase
from services import ContractTypesService

router = APIRouter(
    prefix='/tipos-contratos',
    tags=['tipos-contratos']
)


@router.get('')
def list_contract_types(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return ContractTypesService.list_contract_types(db)

    
@router.post('')
def create_contract_types(payload: ContractTypesCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = ContractTypesService.create_contract_types(payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response_request.dict(), status_code=status.HTTP_400_BAD_REQUEST)

