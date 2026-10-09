import logging
from datetime import datetime, date
from sqlalchemy.orm import Session

from dto.ContractsDTO import ContractsBase, ContractsCreate, ContractListSP
from dto.ResponseRequest import ResponseRequest
from entity.contracts import Contracts as ContractsEntity
from repository import ContractsRepository
from repository import UsuariosRepository
from repository import ContractsRepository as repo
from exceptions import PruebaCreationError, PruebaNotFoundError


def listar(db: Session) -> list[ContractsBase]:
    contratos = ContractsRepository.listar(db)
    return [
        ContractsBase(
            id=int(c.id),
            code=c.code,
            description=c.description,
            year=c.year,
            start_contract_date=c.start_contract_date,
            end_contract_date=c.end_contract_date,
            subscription_date=c.subscription_date,
            policy_date=c.policy_date,
            final_date=c.final_date,
            early_settlement_date=c.early_settlement_date,
            identification_type=c.identification_type,
            identification_number=c.identification_number,
            bank_code=c.bank_code,
            bank_account=c.bank_account,
            address_line_1=c.address_line_1,
            address_line_2=c.address_line_2,
            mobile_phone=c.mobile_phone,
            programa=c.programa.name if c.programa else None,
            contract_type=c.contract_type.description if c.contract_type else None,
            pillar=c.pillar.name if c.pillar else None,
            expense_category=c.expense_category.name if c.expense_category else None,
            purchase_type=c.purchase_type.name if c.purchase_type else None,
            program_id=c.program_id,
            contract_type_id=c.contract_type_id,
            pillar_id=c.pillar_id,
            expense_category_id=c.expense_category_id,
            purchase_type_id=c.purchase_type_id,
            contract_id=c.contract_id,
            terms_reference_id=c.terms_reference_id,
            is_currency_usd=c.is_currency_usd,
            policy_approval=c.policy_approval,
            observations=c.observations,
            causes_early_termination=c.causes_early_termination,
            sharepoint_code_new=c.sharepoint_code_new,
            functions_and_activities=c.functions_and_activities,
            dibursement=c.dibursement,
            monthly_time=c.monthly_time,
            final_duration=c.final_duration,
            value=c.value,
            initial_value=c.initial_value,
            final_value=c.final_value,
            total_adition=c.total_adition,
            released_resource=c.released_resource,
            last_dibursement=c.last_dibursement,
            dibursement_value=c.dibursement_value,
            total_value=c.total_value,
            accumulated_value=c.accumulated_value,
            remaining_value=c.remaining_value,
            created_at=c.created_at,
            updated_at=c.updated_at,
        )
        for c in contratos
    ]

def obtener_por_id(id: int, db: Session) -> ContractsBase | None:
    c = ContractsRepository.obtener_por_id(id, db)
    if not c:
        return None
    return ContractsBase(
                id=int(c.id),
                code=c.code,
                description=c.description,
                year=c.year,
                start_contract_date=c.start_contract_date,
                end_contract_date=c.end_contract_date,
                subscription_date=c.subscription_date,
                policy_date=c.policy_date,
                final_date=c.final_date,
                early_settlement_date=c.early_settlement_date,
                identification_type=c.identification_type,
                identification_number=c.identification_number,
                bank_code=c.bank_code,
                bank_account=c.bank_account,
                address_line_1=c.address_line_1,
                address_line_2=c.address_line_2,
                mobile_phone=c.mobile_phone,
                programa=c.programa.name if c.programa else None,
                contract_type=c.contract_type.description if c.contract_type else None,
                pillar=c.pillar.name if c.pillar else None,
                expense_category=c.expense_category.name if c.expense_category else None,
                purchase_type=c.purchase_type.name if c.purchase_type else None,
                program_id=c.program_id,
                contract_type_id=c.contract_type_id,
                pillar_id=c.pillar_id,
                expense_category_id=c.expense_category_id,
                purchase_type_id=c.purchase_type_id,
                contract_id=c.contract_id,
                terms_reference_id=c.terms_reference_id,
                is_currency_usd=c.is_currency_usd,
                policy_approval=c.policy_approval,
                observations=c.observations,
                causes_early_termination=c.causes_early_termination,
                sharepoint_code_new=c.sharepoint_code_new,
                functions_and_activities=c.functions_and_activities,
                dibursement=c.dibursement,
                monthly_time=c.monthly_time,
                final_duration=c.final_duration,
                value=c.value,
                initial_value=c.initial_value,
                final_value=c.final_value,
                total_adition=c.total_adition,
                released_resource=c.released_resource,
                last_dibursement=c.last_dibursement,
                dibursement_value=c.dibursement_value,
                total_value=c.total_value,
                accumulated_value=c.accumulated_value,
                remaining_value=c.remaining_value,
                created_at=c.created_at,
                updated_at=c.updated_at,
            )

def crear(contrato: ContractsCreate, db: Session, usuario_guid: str) -> ResponseRequest:
    respuesta = ResponseRequest(solicitud_exitosa=True)
    try:
        usuario = UsuariosRepository.obtener_por_guid_msft(usuario_guid.strip(), db)
        if not usuario:
            raise Exception("Usuario no encontrado")
        existe_contrato = ContractsRepository.obtener_por_codigo(contrato.code or '', db)
        if existe_contrato:
            return ResponseRequest(mensaje='Ya existe un contrato con ese código', solicitud_exitosa=False)

        nuevo_contrato = ContractsEntity()
        nuevo_contrato.code = contrato.code
        nuevo_contrato.description = contrato.description
        nuevo_contrato.year = contrato.year
        nuevo_contrato.start_contract_date = contrato.start_contract_date
        nuevo_contrato.end_contract_date = contrato.end_contract_date
        nuevo_contrato.subscription_date = contrato.subscription_date
        nuevo_contrato.policy_date = contrato.policy_date
        nuevo_contrato.final_date = contrato.final_date
        nuevo_contrato.identification_type = contrato.identification_type
        nuevo_contrato.identification_number = contrato.identification_number
        nuevo_contrato.bank_code = contrato.bank_code
        nuevo_contrato.bank_account = contrato.bank_account
        nuevo_contrato.address_line_1 = contrato.address_line_1
        nuevo_contrato.address_line_2 = contrato.address_line_2
        nuevo_contrato.mobile_phone = contrato.mobile_phone
        nuevo_contrato.program_id = contrato.program_id
        nuevo_contrato.contract_type_id = contrato.contract_type_id
        nuevo_contrato.pillar_id = contrato.pillar_id
        nuevo_contrato.expense_category_id = contrato.expense_category_id
        nuevo_contrato.purchase_type_id = contrato.purchase_type_id
        nuevo_contrato.contract_id = contrato.contract_id
        nuevo_contrato.terms_reference_id = contrato.terms_reference_id
        nuevo_contrato.is_currency_usd = contrato.is_currency_usd
        nuevo_contrato.policy_approval = contrato.policy_approval
        nuevo_contrato.observations = contrato.observations
        nuevo_contrato.functions_and_activities = contrato.functions_and_activities
        nuevo_contrato.dibursement = contrato.dibursement
        nuevo_contrato.value = contrato.value
        nuevo_contrato.initial_value = contrato.initial_value
        nuevo_contrato.created_at = datetime.now()
        nuevo_contrato.updated_at = datetime.now()

        db.add(nuevo_contrato)
        db.commit()
        db.refresh(nuevo_contrato)

        respuesta.identity = nuevo_contrato.id
        respuesta.mensaje = "Contrato creado exitosamente"
        return respuesta

    except Exception as e:
        logging.error(f"Error al crear contrato: {e}")
        db.rollback()
        return ResponseRequest(
            solicitud_exitosa=False,
            mensaje=str(e)
        )
        
        
def listar_contracts_sp(
    db: Session,
    page: int,
    filtro: str,
    anio: int = -1,
    tipo: int = -1,
    contrato_padre: int = -1,
) -> list[ContractListSP]:
    try:
        return repo.listar_contracts_sp(
            db, page, filtro, anio, tipo, contrato_padre
        )
    except Exception as e:
        logging.error(f"Failed to list contracts: {str(e)}")
        raise PruebaNotFoundError(str(e))    
    
    
def actualizar(id: int, payload: ContractsCreate, db: Session, usuario_guid: str) -> ResponseRequest:
    try:
        usuario = UsuariosRepository.obtener_por_guid_msft(usuario_guid.strip(), db)
        if not usuario:
            raise Exception("Usuario no encontrado")

        registro = db.query(ContractsEntity).filter(ContractsEntity.id == id).first()
        if not registro:
            return ResponseRequest(solicitud_exitosa=False, mensaje='Contrato no encontrado')

        registro.code = payload.code
        registro.description = payload.description
        registro.year = payload.year
        registro.start_contract_date = payload.start_contract_date
        registro.end_contract_date = payload.end_contract_date
        registro.subscription_date = payload.subscription_date
        registro.policy_date = payload.policy_date
        registro.final_date = payload.final_date
        registro.identification_type = payload.identification_type
        registro.identification_number = payload.identification_number
        registro.bank_code = payload.bank_code
        registro.bank_account = payload.bank_account
        registro.address_line_1 = payload.address_line_1
        registro.address_line_2 = payload.address_line_2
        registro.mobile_phone = payload.mobile_phone
        registro.program_id = payload.program_id
        registro.contract_type_id = payload.contract_type_id
        registro.pillar_id = payload.pillar_id
        registro.expense_category_id = payload.expense_category_id
        registro.purchase_type_id = payload.purchase_type_id
        registro.contract_id = payload.contract_id
        registro.terms_reference_id = payload.terms_reference_id
        registro.is_currency_usd = payload.is_currency_usd
        registro.policy_approval = payload.policy_approval
        registro.observations = payload.observations
        registro.functions_and_activities = payload.functions_and_activities
        registro.dibursement = payload.dibursement
        registro.value = payload.value
        registro.initial_value = payload.initial_value
        registro.updated_at = datetime.now()

        db.commit()
        db.refresh(registro)

        return ResponseRequest(solicitud_exitosa=True, mensaje='Contrato actualizado exitosamente', identity=registro.id)
    except Exception as e:
        db.rollback()
        logging.error(f"Error al actualizar contrato: {e}")
        return ResponseRequest(solicitud_exitosa=False, mensaje=str(e))