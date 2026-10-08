import logging
from sqlalchemy.orm import Session

from dto.AgreementTypesDTO import AgreementTypesBase, AgreementTypesCreateBase
from dto.ResponseRequest import ResponseRequest
from entity.purchase_types import PurchaseTypes
from repository import PurchaseTypesRepository


def list_purchase_types(db: Session) -> list[AgreementTypesBase]:
    purchase_types = PurchaseTypesRepository.list_purchase_types(db)
    return [
        AgreementTypesBase(
            id=int(m.id),
            name= m.name,
            origen=m.origen,
            description= m.description,
            color= m.color,
            
        )
        for m in purchase_types
    ]



def create_purchase_types(payload: AgreementTypesCreateBase, db: Session) -> ResponseRequest:
    try:
        existente = PurchaseTypesRepository(payload.name or '', db)
        if existente:
            return ResponseRequest(mensaje='Ya existe un tipo de contratación  con ese nombre', solicitud_exitosa=False)

        nuevo = PurchaseTypes(name=(payload.name or '').strip())
        creado = PurchaseTypesRepository.create_purchase_types(nuevo, db)
        return ResponseRequest(mensaje='tipo de contratación creado exitosamente', identity=int(creado.id), solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error creating purchase types: {str(e)}")
        return ResponseRequest(mensaje='Error al crear tipo de contratación ', solicitud_exitosa=False)

