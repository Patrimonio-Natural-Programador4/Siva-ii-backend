import logging
from sqlalchemy.orm import Session

from dto.ImplementersDto  import ImplementerBase, ImplementerCreateBase
from dto.ResponseRequest import ResponseRequest
from entity.implementers import Implementers
from repository import ImplementersRepository


def listar_implementadoras(db: Session) -> list[ImplementerBase]:
    implementadoras = ImplementersRepository.listar_implementadoras(db)
    return [
        ImplementerBase(
            id=int(p.id),
            acronym=p.acronym,
            identification_type=p.identification_type,
            type_id=p.type_id,
        )
        for p in implementadoras
    ]


def obtener_implementadora_por_id(id: int, db: Session) -> ImplementerBase | None:
    implementadora = ImplementersRepository.obtener_implemntadora_por_id(id, db)
    if not implementadora:
        return None
    return ImplementerBase(
        id=int(implementadora.id),
        acronym=implementadora.acronym,
        identification_type=implementadora.identification_type,
        type_id=implementadora.type_id,
    )


def crear_implementadora(payload: ImplementerCreateBase, db: Session) -> ResponseRequest:
    try:
        existente = ImplementersRepository.obtener_implemntadora_por_acronimo(payload.name or '', db)
        if existente:
            return ResponseRequest(mensaje='Ya existe un implementadora con ese nombre', solicitud_exitosa=False)

        nuevo = Implementers(
            name=(payload.name or '').strip(),
            acronym=payload.acronym,
            identification_type=payload.identification_type,
            type_id=payload.type_id,
        )
        creado = ImplementersRepository.crear_implementadora(nuevo, db)
        return ResponseRequest(mensaje='implementadora creado exitosamente', identity=int(creado.id), solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error creating implementadora: {str(e)}")
        return ResponseRequest(mensaje='Error al crear el implementadora', solicitud_exitosa=False)


def actualizar_implementadora(id: int, payload: ImplementerCreateBase, db: Session) -> ResponseRequest:
    try:
        implementadora = ImplementersRepository.obtener_implementadora_por_id(id, db)
        if not implementadora:
            return ResponseRequest(mensaje='implementadora no encontrado', solicitud_exitosa=False)

        nombre_nuevo = (payload.name or '').strip()
        if nombre_nuevo.lower() != (implementadora.name or '').lower():
            existente = ImplementersRepository.obtener_implementadora_por_nombre(nombre_nuevo, db)
            if existente:
                return ResponseRequest(mensaje='Ya existe un implementadora con ese nombre', solicitud_exitosa=False)

        implementadora.name = nombre_nuevo
        implementadora.description = payload.description
        implementadora.color = payload.color

        ImplementersRepository.actualizar_implementadora(implementadora, db)
        return ResponseRequest(mensaje='implementadora actualizado exitosamente', identity=id, solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error updating implementadora: {str(e)}")
        return ResponseRequest(mensaje='Error al actualizar el implementadora', solicitud_exitosa=False)
