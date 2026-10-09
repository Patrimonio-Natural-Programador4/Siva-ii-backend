import logging
from sqlalchemy.orm import Session

from dto.ExpenseCategories import ExpenseCategoriesBase, ExpenseCategoriesCreateBase
from dto.ResponseRequest import ResponseRequest
from entity.expense_categories import ExpenseCategories
from repository import ExpenseCategoriesRepository


def list_expense_categories(db: Session) -> list[ExpenseCategoriesBase]:
    expense_categories = ExpenseCategoriesRepository.list_expense_categories(db)
    return [
        ExpenseCategoriesBase(
            id=int(m.id),
            name= m.name,
            description= m.description,
            
        )
        for m in expense_categories
    ]



def create_expense_categories(payload: ExpenseCategoriesCreateBase, db: Session) -> ResponseRequest:
    try:
        existente = ExpenseCategoriesRepository(payload.name or '', db)
        if existente:
            return ResponseRequest(mensaje='Ya existe una categoría de gasto con ese nombre', solicitud_exitosa=False)

        nuevo = ExpenseCategories(name=(payload.name or '').strip())
        creado = ExpenseCategoriesRepository.create_expense_categories(nuevo, db)
        return ResponseRequest(mensaje='categoría de gasto creada exitosamente', identity=int(creado.id), solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error creating expense categories: {str(e)}")
        return ResponseRequest(mensaje='Error al crear categoría de gasto ', solicitud_exitosa=False)

