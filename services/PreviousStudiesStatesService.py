import logging
from sqlalchemy.orm import Session

from dto.PreviousStudiesStatesDTO import PreviousStudiesStatesBase, PreviousStudiesStatesCreateBase
from dto.ResponseRequest import ResponseRequest
from entity.previous_studies_states import PreviousStudiesStates
from repository import PreviousStudiesStatesRepository


def listar_estudios_previos_estado(db: Session) -> list[PreviousStudiesStatesBase]:
    estudio = PreviousStudiesStatesRepository.listar_estudios_previos_estado(db)
    return [
        PreviousStudiesStatesBase(
            id=int(p.id),
            state=p.state,
            
        )
        for p in estudio
    ]


def obtener_estudios_previos_estado_por_id(id: int, db: Session) -> PreviousStudiesStatesBase | None:
    estudio = PreviousStudiesStatesRepository.obtener_estudios_previos_estado_por_id(id, db)
    if not estudio:
        return None
    return PreviousStudiesStatesBase(
        id=int(estudio.id),
        state=estudio.state,
       
    )


def crear_estudios_previos_estado(payload: PreviousStudiesStatesCreateBase, db: Session) -> ResponseRequest:
    try:
        existente = PreviousStudiesStatesRepository.obtener_estudios_previos_estado_por_estado(payload.state or '', db)
        if existente:
            return ResponseRequest(mensaje='Ya existe un estado con ese nombre', solicitud_exitosa=False)

        nuevo = PreviousStudiesStates(
            state=(payload.state or '').strip(),
            
        )
        creado = PreviousStudiesStatesRepository.crear_estudios_previos_estado(nuevo, db)
        return ResponseRequest(mensaje='estado creado exitosamente', identity=int(creado.id), solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error creating state: {str(e)}")
        return ResponseRequest(mensaje='Error al crear el estado', solicitud_exitosa=False)


def actualizar_estudios_previos_estado(id: int, payload: PreviousStudiesStatesCreateBase, db: Session) -> ResponseRequest:
    try:
        estudio = PreviousStudiesStatesRepository.obtener_estudios_previos_estado_por_id(id, db)
        if not estudio:
            return ResponseRequest(mensaje='estado no encontrado', solicitud_exitosa=False)

        nombre_nuevo = (payload.state or '').strip()
        if nombre_nuevo.lower() != (estudio.state or '').lower():
            existente = PreviousStudiesStatesRepository.obtener_estudios_previos_estado_por_estado(nombre_nuevo, db)
            if existente:
                return ResponseRequest(mensaje='Ya existe un estado con ese nombre', solicitud_exitosa=False)

        estudio.state = nombre_nuevo
       

        PreviousStudiesStatesRepository.actualizar_estudios_previos_estado(estudio, db)
        return ResponseRequest(mensaje='estado actualizado exitosamente', identity=id, solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error updating estado: {str(e)}")
        return ResponseRequest(mensaje='Error al actualizar el estado', solicitud_exitosa=False)
