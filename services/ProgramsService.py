import logging
from sqlalchemy.orm import Session

from dto.ProgramsDTO import ProgramsBase, ProgramsCreateBase
from dto.ResponseRequest import ResponseRequest
from entity.programs import Programs
from repository import ProgramsRepository


def listar_programas(db: Session) -> list[ProgramsBase]:
    programas = ProgramsRepository.listar(db)
    return [
        ProgramsBase(
            id_programa=int(p.id),
            name=p.name,
            description=p.description,
            code=p.code,
        )
        for p in programas
    ]


def obtener_programa_por_id(id_programa: int, db: Session) -> ProgramsBase | None:
    programa = ProgramsRepository.obtener_por_id(id_programa, db)
    if not programa:
        return None
    return ProgramsBase(
        id_programa=int(programa.id),
        name=programa.name,
        description=programa.description,
        code=programa.code,
    )


def crear_programa(payload: ProgramsCreateBase, db: Session) -> ResponseRequest:
    try:
        existente = ProgramsRepository.obtener_por_nombre(payload.name or '', db)
        if existente:
            return ResponseRequest(mensaje='Ya existe un programa con ese nombre', solicitud_exitosa=False)

        nuevo = Programs(
            name=(payload.name or '').strip(),
            description=payload.description,
            code=payload.code,
        )
        creado = ProgramsRepository.crear(nuevo, db)
        return ResponseRequest(mensaje='Programa creado exitosamente', identity=int(creado.id), solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error creating program: {str(e)}")
        return ResponseRequest(mensaje='Error al crear el programa', solicitud_exitosa=False)


def actualizar_programa(id_programa: int, payload: ProgramsCreateBase, db: Session) -> ResponseRequest:
    try:
        programa = ProgramsRepository.obtener_por_id(id_programa, db)
        if not programa:
            return ResponseRequest(mensaje='Programa no encontrado', solicitud_exitosa=False)

        nombre_nuevo = (payload.name or '').strip()
        if nombre_nuevo.lower() != (programa.name or '').lower():
            existente = ProgramsRepository.obtener_por_nombre(nombre_nuevo, db)
            if existente:
                return ResponseRequest(mensaje='Ya existe un programa con ese nombre', solicitud_exitosa=False)

        programa.name = nombre_nuevo
        programa.description = payload.description
        programa.code = payload.code

        ProgramsRepository.actualizar(programa, db)
        return ResponseRequest(mensaje='Programa actualizado exitosamente', identity=id_programa, solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error updating program: {str(e)}")
        return ResponseRequest(mensaje='Error al actualizar el programa', solicitud_exitosa=False)
