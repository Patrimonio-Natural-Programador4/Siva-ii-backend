import logging
from sqlalchemy.orm import Session

from dto.ProductsStateDTO import ProductsStateBase, ProductsStateCreateBase
from dto.ResponseRequest import ResponseRequest
from entity.products_state import ProductsState
from repository import ProductsStateRepository


def list_products_state(db: Session) -> list[ProductsStateBase]:
    state = ProductsStateRepository.list_products_state(db)
    return [
        ProductsStateBase(
            id=int(p.id),
            name=p.name,
            color= p.color,
            
        )
        for p in state
    ]


def get_products_state_by_id(id: int, db: Session) -> ProductsStateBase | None:
    state = ProductsStateRepository.get_products_state_by_id(id, db)
    if not state:
        return None
    return ProductsStateBase(
        id=int(state.id),
        name=state.name,
        color=state.color,
       
    )


def create_products_state(payload: ProductsStateCreateBase, db: Session) -> ResponseRequest:
    try:
        existente = ProductsStateRepository.get_products_state_by_state(payload.name or '', db)
        if existente:
            return ResponseRequest(mensaje='Ya existe un estado con ese nombre', solicitud_exitosa=False)

        nuevo = ProductsState(
            name=(payload.name or '').strip(),
            color=payload.color,
            
        )
        creado = ProductsStateRepository.create_products_state(nuevo, db)
        return ResponseRequest(mensaje='Estado creado exitosamente', identity=int(creado.id), solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error creating state: {str(e)}")
        return ResponseRequest(mensaje='Error al crear el estado', solicitud_exitosa=False)


def update_products_state(id: int, payload: ProductsStateCreateBase, db: Session) -> ResponseRequest:
    try:
        state = ProductsStateRepository.get_products_state_by_id(id, db)
        if not state:
            return ResponseRequest(mensaje='Estado no encontrado', solicitud_exitosa=False)

        nombre_nuevo = (payload.name or '').strip()
        if nombre_nuevo.lower() != (state.name or '').lower():
            existente = ProductsStateRepository.get_products_state_by_state(nombre_nuevo, db)
            if existente:
                return ResponseRequest(mensaje='Ya existe un estado con ese nombre', solicitud_exitosa=False)

        state.name = nombre_nuevo
        state.color= payload.color
       

        ProductsStateRepository.update_products_state(state, db)
        return ResponseRequest(mensaje='Estado actualizado exitosamente', identity=id, solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error updating estado: {str(e)}")
        return ResponseRequest(mensaje='Error al actualizar el estado', solicitud_exitosa=False)
