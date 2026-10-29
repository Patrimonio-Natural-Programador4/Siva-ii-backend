import logging
from sqlalchemy.orm import Session

from dto.DisbursementStateDTO import DisbursementStateBase, DisbursementStateCreateBase
from dto.ResponseRequest import ResponseRequest
from entity.disbursement_state import DisbursementState
from repository import DisbursementStateRepository


def list_disbursement_state(db: Session) -> list[DisbursementStateBase]:
    state = DisbursementStateRepository.list_disbursement_state(db)
    return [
        DisbursementStateBase(
            id=int(p.id),
            name=p.name,
            color= p.color,
            
        )
        for p in state
    ]


def get_disbursement_state_by_id(id: int, db: Session) -> DisbursementStateBase | None:
    state = DisbursementStateRepository.get_disbursement_state_by_id(id, db)
    if not state:
        return None
    return DisbursementStateBase(
        id=int(state.id),
        name=state.name,
        color=state.color,
       
    )


def create_disbursement_state(payload: DisbursementStateCreateBase, db: Session) -> ResponseRequest:
    try:
        existente = DisbursementStateRepository.get_disbursement_state_by_state(payload.name or '', db)
        if existente:
            return ResponseRequest(mensaje='Ya existe un estado con ese nombre', solicitud_exitosa=False)

        nuevo = DisbursementState(
            name=(payload.name or '').strip(),
            color=payload.color,
            
        )
        creado = DisbursementStateRepository.create_disbursement_state(nuevo, db)
        return ResponseRequest(mensaje='Estado creado exitosamente', identity=int(creado.id), solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error creating state: {str(e)}")
        return ResponseRequest(mensaje='Error al crear el estado', solicitud_exitosa=False)


def update_disbursement_state(id: int, payload: DisbursementStateCreateBase, db: Session) -> ResponseRequest:
    try:
        state = DisbursementStateRepository.get_disbursement_state_by_id(id, db)
        if not state:
            return ResponseRequest(mensaje='Estado no encontrado', solicitud_exitosa=False)

        nombre_nuevo = (payload.name or '').strip()
        if nombre_nuevo.lower() != (state.name or '').lower():
            existente = DisbursementStateRepository.get_disbursement_state_by_state(nombre_nuevo, db)
            if existente:
                return ResponseRequest(mensaje='Ya existe un estado con ese nombre', solicitud_exitosa=False)

        state.name = nombre_nuevo
        state.color= payload.color
       

        DisbursementStateRepository.update_disbursement_state(state, db)
        return ResponseRequest(mensaje='Estado actualizado exitosamente', identity=id, solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error updating estado: {str(e)}")
        return ResponseRequest(mensaje='Error al actualizar el estado', solicitud_exitosa=False)
