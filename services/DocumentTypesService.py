import logging
from sqlalchemy.orm import Session

from dto.DocumentTypesDTO import DocumentypesBase, DocumentypeCreateBase
from dto.ResponseRequest import ResponseRequest
from entity.programs import Programs
from repository import DocumentypesRepository


def listar_tipos_documentos(db: Session) -> list[DocumentypesBase]:
    document_types = DocumentypesRepository.listar(db)
    return [
        DocumentypesBase(
            id=int(p.id),
            name=p.name,
            description=p.description,
            code=p.code,
        )
        for p in document_types
    ]


def obtener_tipo_documento_por_id(id: int, db: Session) -> DocumentypesBase | None:
    docu = DocumentypesRepository.obtener_por_id(id, db)
    if not docu:
        return None
    return DocumentypesBase(
        id=int(docu.id),
        name=docu.name,
        description=docu.description,
        code=docu.code,
    )


def crear_tipo_documento(payload: DocumentypeCreateBase, db: Session) -> ResponseRequest:
    try:
        existente = DocumentypesRepository.obtener_por_nombre(payload.name or '', db)
        if existente:
            return ResponseRequest(mensaje='Ya existe un tipo de documento con ese nombre', solicitud_exitosa=False)

        nuevo = Programs(
            name=(payload.name or '').strip(),
            description=payload.description,
            code=payload.code,
        )
        creado = DocumentypesRepository.crear(nuevo, db)
        return ResponseRequest(mensaje='tipo de documento  creado exitosamente', identity=int(creado.id), solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error creating program: {str(e)}")
        return ResponseRequest(mensaje='Error al crear el tipo de documento ', solicitud_exitosa=False)


def actualizar_tipo_documento(id_programa: int, payload: DocumentypeCreateBase, db: Session) -> ResponseRequest:
    try:
        programa = DocumentypesRepository.obtener_por_id(id_programa, db)
        if not programa:
            return ResponseRequest(mensaje='tipo de documento  no encontrado', solicitud_exitosa=False)

        nombre_nuevo = (payload.name or '').strip()
        if nombre_nuevo.lower() != (programa.name or '').lower():
            existente = DocumentypesRepository.obtener_por_nombre(nombre_nuevo, db)
            if existente:
                return ResponseRequest(mensaje='Ya existe un tipo de documento  con ese nombre', solicitud_exitosa=False)

        programa.name = nombre_nuevo
        programa.description = payload.description
        programa.code = payload.code

        DocumentypesRepository.actualizar(programa, db)
        return ResponseRequest(mensaje='tipo de documento  actualizado exitosamente', identity=id_programa, solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error updating program: {str(e)}")
        return ResponseRequest(mensaje='Error al actualizar el tipo de documento ', solicitud_exitosa=False)
