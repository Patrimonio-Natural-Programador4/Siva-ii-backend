import logging
from sqlalchemy.orm import Session

from dto.CodesDTO import CodesBase, CodesCreateBase
from dto.ResponseRequest import ResponseRequest
from entity.codes import Codes
from repository import CodesRepository


def list_codes(db: Session) -> list[CodesBase]:
    codes = CodesRepository.list_codes(db)
    return [
        CodesBase(
            id=int(m.id),
            code= m.code,
            origin= m.origin,
            
        )
        for m in codes
    ]



def create_codes(payload: CodesCreateBase, db: Session) -> ResponseRequest:
    try:
        existente = CodesRepository(payload.code or '', db)
        if existente:
            return ResponseRequest(mensaje='Ya existe un código con ese código', solicitud_exitosa=False)

        nuevo = Codes(name=(payload.code or '').strip())
        creado = CodesRepository.create_codes(nuevo, db)
        return ResponseRequest(mensaje='Código creado exitosamente', identity=int(creado.id), solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error creating codes: {str(e)}")
        return ResponseRequest(mensaje='Error al crear código ', solicitud_exitosa=False)

