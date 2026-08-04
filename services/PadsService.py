import logging
from sqlalchemy.orm import Session

from dto.PadsDTO import PadsBase, PadsCreateBase
from dto.ResponseRequest import ResponseRequest
from entity.pads import Pads
from repository import PadsRepository


def listar_pads(db: Session) -> list[PadsBase]:
    pads = PadsRepository.listar(db)
    return [
        PadsBase(
            id=int(p.id),
            name=p.name,
            description=p.description,
            color=p.color,
        )
        for p in pads
    ]


def obtener_pad_por_id(id: int, db: Session) -> PadsBase | None:
    pad = PadsRepository.obtener_pad_por_id(id, db)
    if not pad:
        return None
    return PadsBase(
        id=int(pad.id),
        name=pad.name,
        description=pad.description,
        color=pad.color,
    )


def crear_pad(payload: PadsCreateBase, db: Session) -> ResponseRequest:
    try:
        existente = PadsRepository.obtener_pad_por_nombre(payload.name or '', db)
        if existente:
            return ResponseRequest(mensaje='Ya existe un pad con ese nombre', solicitud_exitosa=False)

        nuevo = Pads(
            name=(payload.name or '').strip(),
            description=payload.description,
            color=payload.color,
        )
        creado = PadsRepository.crear_pad(nuevo, db)
        return ResponseRequest(mensaje='pad creado exitosamente', identity=int(creado.id), solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error creating pad: {str(e)}")
        return ResponseRequest(mensaje='Error al crear el pad', solicitud_exitosa=False)


def actualizar_pad(id: int, payload: PadsCreateBase, db: Session) -> ResponseRequest:
    try:
        pad = PadsRepository.obtener_pad_por_id(id, db)
        if not pad:
            return ResponseRequest(mensaje='pad no encontrado', solicitud_exitosa=False)

        nombre_nuevo = (payload.name or '').strip()
        if nombre_nuevo.lower() != (pad.name or '').lower():
            existente = PadsRepository.obtener_pad_por_nombre(nombre_nuevo, db)
            if existente:
                return ResponseRequest(mensaje='Ya existe un pad con ese nombre', solicitud_exitosa=False)

        pad.name = nombre_nuevo
        pad.description = payload.description
        pad.color = payload.color

        PadsRepository.actualizar_pad(pad, db)
        return ResponseRequest(mensaje='pad actualizado exitosamente', identity=id, solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error updating pad: {str(e)}")
        return ResponseRequest(mensaje='Error al actualizar el pad', solicitud_exitosa=False)
