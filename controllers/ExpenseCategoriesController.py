from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.ExpenseCategories import ExpenseCategoriesBase, ExpenseCategoriesCreateBase
from services import ExpenseCategoriesService

router = APIRouter(
    prefix='/categoria-gasto',
    tags=['categoria-gasto']
)


@router.get('')
def list_expense_categories(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return ExpenseCategoriesService.list_expense_categories(db)

    
@router.post('')
def create_ExpenseCategories(payload: ExpenseCategoriesCreateBase, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    response_request = ExpenseCategoriesService.create_expense_categories(payload, db)

    if response_request.solicitud_exitosa:
        return JSONResponse(content=response_request.dict(), status_code=status.HTTP_200_OK)

    return JSONResponse(content=response_request.dict(), status_code=status.HTTP_400_BAD_REQUEST)

