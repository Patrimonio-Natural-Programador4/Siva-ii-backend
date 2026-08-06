import logging
from sqlalchemy.orm import Session

from dto.PersonsDTO  import PersonBase,PersonCreateBase
from dto.ResponseRequest import ResponseRequest
from entity.implementers import Implementers
from repository import PersonsRepository


def listar(db: Session) -> list[PersonBase]:
    perons = PersonsRepository.listar(db)
    return [
        PersonBase(
            id=int(p.id),
            first_name=p.first_name,
            other_name=p.other_name,
            last_name=p.last_name,
            other_last_name=p.other_last_name,
            email=p.email,
            phone=p.phone,
            identification_type=p.identification_type,
            
        )
        for p in perons
    ]

"""
def crear(payload: PersonCreateBase, db: Session) -> ResponseRequest:
    try:
        existente = PersonsRepository.obtener_implemntadora_por_acronimo(payload.name or '', db)
        if existente:
            return ResponseRequest(mensaje='Ya existe un implementadora con ese nombre', solicitud_exitosa=False)

        nuevo = Implementers(
            name=(payload.name or '').strip(),
            acronym=payload.acronym,
            identification_type=payload.identification_type,
            type_id=payload.type_id,
        )
        creado = PersonsRepository.crear_implementadora(nuevo, db)
        return ResponseRequest(mensaje='implementadora creado exitosamente', identity=int(creado.id), solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error creating implementadora: {str(e)}")
        return ResponseRequest(mensaje='Error al crear el implementadora', solicitud_exitosa=False)

"""