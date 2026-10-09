import logging
from sqlalchemy.orm import Session

from dto.AgreementTypesDTO import AgreementTypesBase, AgreementTypesCreateBase
from dto.ResponseRequest import ResponseRequest
from entity.agreement_types import AgreementTypes
from repository import AgreementTypesRepository


def list_agreement_types(db: Session) -> list[AgreementTypesBase]:
    agreement_types = AgreementTypesRepository.list_agreement_types(db)
    return [
        AgreementTypesBase(
            id=int(m.id),
            name= m.name,
            code= m.code,
            description= m.description,
            is_frame=m.is_frame,
            is_independent= m.is_independent,
            color= m.color,
            
        )
        for m in agreement_types
    ]



def create_agreement_types(payload: AgreementTypesCreateBase, db: Session) -> ResponseRequest:
    try:
        existente = AgreementTypesRepository.get_by_name_agreement_types(payload.name or '', db)
        if existente:
            return ResponseRequest(mensaje='Ya existe un tipo de acuerdo con ese nombre', solicitud_exitosa=False)

        nuevo = AgreementTypes(name=(payload.name or '').strip())
        creado = AgreementTypesRepository.create_agreement_types(nuevo, db)
        return ResponseRequest(mensaje='tipo de acuerdo creado exitosamente', identity=int(creado.id), solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error creating agreement_types: {str(e)}")
        return ResponseRequest(mensaje='Error al crear tipo de acuerdo', solicitud_exitosa=False)

