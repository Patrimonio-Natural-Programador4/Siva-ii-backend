import logging
from sqlalchemy.orm import Session

from dto.CapacityAssessmentsStatesDTO import CapacityAssessmentsStatesBase, CapacityAssessmentsStatesCreateBase
from dto.ResponseRequest import ResponseRequest
from entity.capacity_assessments_states import CapacityAssessmentsStates
from repository import CapacityAssessmentsStatesRepository


def listar_capacity_assessments_states(db: Session) -> list[CapacityAssessmentsStatesBase]:
    evaluacion = CapacityAssessmentsStatesRepository.listar(db)
    return [
        CapacityAssessmentsStatesBase(
            id=int(p.id),
            state=p.state,
            
        )
        for p in evaluacion
    ]


def obtener_capacity_assessments_states_por_id(id: int, db: Session) -> CapacityAssessmentsStatesBase | None:
    evaluacion = CapacityAssessmentsStatesRepository.obtener_capacity_assessments_states_por_id(id, db)
    if not evaluacion:
        return None
    return CapacityAssessmentsStatesBase(
        id=int(evaluacion.id),
        state=evaluacion.state,
       
    )


def crear_capacity_assessments_states(payload: CapacityAssessmentsStatesCreateBase, db: Session) -> ResponseRequest:
    try:
        existente = CapacityAssessmentsStatesRepository.obtener_capacity_assessments_states_por_estado(payload.state or '', db)
        if existente:
            return ResponseRequest(mensaje='Ya existe un estado con ese nombre', solicitud_exitosa=False)

        nuevo = CapacityAssessmentsStates(
            state=(payload.state or '').strip(),
            
        )
        creado = CapacityAssessmentsStatesRepository.crear_capacity_assessments_states(nuevo, db)
        return ResponseRequest(mensaje='estado creado exitosamente', identity=int(creado.id), solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error creating state: {str(e)}")
        return ResponseRequest(mensaje='Error al crear el estado', solicitud_exitosa=False)


def actualizar_capacity_assessments_states(id: int, payload: CapacityAssessmentsStatesCreateBase, db: Session) -> ResponseRequest:
    try:
        evaluacion = CapacityAssessmentsStatesRepository.obtener_capacity_assessments_states_por_id(id, db)
        if not evaluacion:
            return ResponseRequest(mensaje='estado no encontrado', solicitud_exitosa=False)

        nombre_nuevo = (payload.state or '').strip()
        if nombre_nuevo.lower() != (evaluacion.state or '').lower():
            existente = CapacityAssessmentsStatesRepository.obtener_capacity_assessments_states_por_estado(nombre_nuevo, db)
            if existente:
                return ResponseRequest(mensaje='Ya existe un estado con ese nombre', solicitud_exitosa=False)

        evaluacion.state = nombre_nuevo
       

        CapacityAssessmentsStatesRepository.actualizar_capacity_assessments_states(evaluacion, db)
        return ResponseRequest(mensaje='estado actualizado exitosamente', identity=id, solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error updating estado: {str(e)}")
        return ResponseRequest(mensaje='Error al actualizar el estado', solicitud_exitosa=False)
