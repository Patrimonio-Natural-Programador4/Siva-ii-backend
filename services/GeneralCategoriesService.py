import logging
from sqlalchemy.orm import Session

from dto.ExpenseCategories import ExpenseCategoriesBase, ExpenseCategoriesCreateBase
from dto.ResponseRequest import ResponseRequest
from entity.general_categories import GeneralCategories
from repository import GeneralCategoriesRepository


def list_general_categories(db: Session) -> list[ExpenseCategoriesBase]:
    expense_categories = GeneralCategoriesRepository.list_general_categories(db)
    return [
        ExpenseCategoriesBase(
            id=int(m.id),
            name= m.name,
            
            
        )
        for m in expense_categories
    ]



def create_general_categories(payload: ExpenseCategoriesCreateBase, db: Session) -> ResponseRequest:
    try:
        existente = GeneralCategoriesRepository(payload.name or '', db)
        if existente:
            return ResponseRequest(mensaje='Ya existe una categoría general con ese nombre', solicitud_exitosa=False)

        nuevo = GeneralCategories(name=(payload.name or '').strip())
        creado = GeneralCategoriesRepository.create_general_categories(nuevo, db)
        return ResponseRequest(mensaje='categoría general creada exitosamente', identity=int(creado.id), solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error creating general categories: {str(e)}")
        return ResponseRequest(mensaje='Error al crear categoría general ', solicitud_exitosa=False)

