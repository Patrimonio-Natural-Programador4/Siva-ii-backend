import logging
from sqlalchemy.orm import Session

from dto.AgreementOriginsDTO import AgreementOriginsBase, AgreementOriginsCreateBase
from dto.ResponseRequest import ResponseRequest
from entity.agreement_origins import AgreementOrigins
from repository import AgreementOriginsRepository


def list_agreement_origins(db: Session) -> list[AgreementOriginsBase]:
    agreement_origins = AgreementOriginsRepository.list_agreement_origins(db)
    return [
        AgreementOriginsBase(
            id=int(m.id),
            name=m.name,
            description=m.description,
            color= m.color
        )
        for m in agreement_origins
    ]



def create_agreement_origins (payload: AgreementOriginsCreateBase, db: Session) -> ResponseRequest:
    try:
        existente = AgreementOriginsRepository.get_by_name_agreement_origins(payload.name or '', db)
        if existente:
            return ResponseRequest(mensaje='Ya existe una origen acuerdo con ese nombre', solicitud_exitosa=False)

        nuevo = AgreementOrigins(name=(payload.name or '').strip())
        creado = AgreementOriginsRepository.create_agreement_origins(nuevo, db)
        return ResponseRequest(mensaje='origen acuerdo creada exitosamente', identity=int(creado.id), solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error creating Agreement origins: {str(e)}")
        return ResponseRequest(mensaje='Error al crear la origen acuerdo', solicitud_exitosa=False)

