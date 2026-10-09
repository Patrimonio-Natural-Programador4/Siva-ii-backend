import logging
from sqlalchemy.orm import Session

from dto.ContractTypesDTO import ContractTypesBase, ContractTypesCreateBase
from dto.ResponseRequest import ResponseRequest
from entity.contract_types import ContractTypes
from repository import ContractTypesRepository


def list_contract_types(db: Session) -> list[ContractTypesBase]:
    contract_types = ContractTypesRepository.list_contract_types(db)
    return [
        ContractTypesBase(
            id=int(m.id),
            name= m.name,
            code= m.code,
            description= m.description,
            color= m.color,
            
        )
        for m in contract_types
    ]



def create_contract_types(payload: ContractTypesCreateBase, db: Session) -> ResponseRequest:
    try:
        existente = ContractTypesRepository.get_by_name_contract_types(payload.name or '', db)
        if existente:
            return ResponseRequest(mensaje='Ya existe un tipo de contrato con ese nombre', solicitud_exitosa=False)

        nuevo = ContractTypes(name=(payload.name or '').strip())
        creado = ContractTypesRepository.create_contract_types(nuevo, db)
        return ResponseRequest(mensaje='tipo de contrato creado exitosamente', identity=int(creado.id), solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error creating contract_types: {str(e)}")
        return ResponseRequest(mensaje='Error al crear tipo de contrato', solicitud_exitosa=False)

