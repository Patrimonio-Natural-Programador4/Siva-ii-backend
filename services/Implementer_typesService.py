import logging
from sqlalchemy.orm import Session

from dto.ImplementerTypesDTO import Implementer_typesBase,Implementer_typesCreateBase,Implementer_typesUpdateBase
from dto.ResponseRequest import ResponseRequest
from entity.implementer_types import Implementer_types
from repository import Implementer_typesRepository


def listar_tipos_implementadora(db: Session) -> list[Implementer_typesBase]:
    tipos_implementadora = Implementer_typesRepository.listar(db)
    return [
        Implementer_typesBase(
            id=int(p.id),
            name=p.name,
           
        )
        for p in tipos_implementadora
    ]


def obtener_tipos_implementadora_por_id(id: int, db: Session) -> Implementer_typesBase | None:
    tipos_implementadora = Implementer_typesRepository.obtener_tipos_implementadora_por_id(id, db)
    if not tipos_implementadora:
        return None
    return Implementer_typesBase(
        id=int(tipos_implementadora.id),
        name=tipos_implementadora.name,
       
    )


def crear_tipos_implementadora(payload: Implementer_typesCreateBase, db: Session) -> ResponseRequest:
    try:
        existente = Implementer_typesRepository.obtener_tipos_implementadora_por_name(payload.name or '', db)
        if existente:
            return ResponseRequest(mensaje='Ya existe un tipo de implementadora con ese nombre', solicitud_exitosa=False)

        nuevo = Implementer_types(
            name=(payload.name or '').strip(),
            
        )
        creado = Implementer_typesRepository.crear_tipos_implementadora(nuevo, db)
        return ResponseRequest(mensaje='Tipo implementadora creado exitosamente', identity=int(creado.id), solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error creating implementer_types: {str(e)}")
        return ResponseRequest(mensaje='Error al crear el tipo implementadora', solicitud_exitosa=False)


def actualizar_tipos_implementadora(id: int, payload: Implementer_typesCreateBase, db: Session) -> ResponseRequest:
    try:
        tipos_implementadora = Implementer_typesRepository.obtener_tipos_implementadora_por_id(id, db)
        if not tipos_implementadora:
            return ResponseRequest(mensaje='Tipo implementadora no encontrado', solicitud_exitosa=False)

        nombre_nuevo = (payload.name or '').strip()
        if nombre_nuevo.lower() != (tipos_implementadora.name or '').lower():
            existente = Implementer_typesRepository.obtener_tipos_implementadora_por_name(nombre_nuevo, db)
            if existente:
                return ResponseRequest(mensaje='Ya existe un tipo de implementadora con ese nombre', solicitud_exitosa=False)

        tipos_implementadora.name = nombre_nuevo
       

        Implementer_typesRepository.actualizar(tipos_implementadora, db)
        return ResponseRequest(mensaje='Tipo implementadora actualizado exitosamente', identity=id, solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error updating implementer types: {str(e)}")
        return ResponseRequest(mensaje='Error al actualizar el tipo implementadora', solicitud_exitosa=False)
