import logging
from sqlalchemy.orm import Session

from dto.PadStatusDTO import PadStatusBase, PadStatusCreateBase
from dto.ResponseRequest import ResponseRequest
from entity.padstatus import PadStatus
from repository import PadStatusRepository


def list_pad_status(db: Session) -> list[PadStatusBase]:
    pad_status = PadStatusRepository.list_pad_status(db)
    return [
        PadStatusBase(
            id=int(m.id),
            name= m.name,
            status= m.status,
            
        )
        for m in pad_status
    ]



def create_pad_status(payload: PadStatusCreateBase, db: Session) -> ResponseRequest:
    try:
        existente = PadStatusRepository(payload.name or '', db)
        if existente:
            return ResponseRequest(mensaje='Ya existe un estado con ese nombre', solicitud_exitosa=False)

        nuevo = PadStatus(name=(payload.name or '').strip())
        creado = PadStatusRepository.create_pad_status(nuevo, db)
        return ResponseRequest(mensaje='Estado creado exitosamente', identity=int(creado.id), solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error creating pad status: {str(e)}")
        return ResponseRequest(mensaje='Error al crear estado ', solicitud_exitosa=False)

