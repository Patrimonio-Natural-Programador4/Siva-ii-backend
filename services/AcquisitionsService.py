import logging
from datetime import datetime
from sqlalchemy.orm import Session

from dto.AcquisitionsDTO import AcquisitionsBase, AcquisitionsCreate, AcquisitionListSP
from dto.ResponseRequest import ResponseRequest
from entity.acquisitions import Acquisitions as AcquisitionsEntity
from repository import AcquisitionsRepository 
from repository import UsuariosRepository
from exceptions import PruebaNotFoundError


def list_acquisitions(db: Session) -> list[AcquisitionsBase]:
    acquisitions = AcquisitionsRepository.list_acquisitions(db)
    return [
        AcquisitionsBase(
            id=int(a.id),
            process_number=a.process_number,
            type=a.type,
            description=a.description,
            numero_contrato_temporal=a.numero_contrato_temporal,
            status=a.status,
            contracts_qty=a.contracts_qty,
            activity_id=a.activity_id,
            activity_code=a.activity.code if a.activity else None,
            activity_description=a.activity.description if a.activity else None,
            expense_category_id=a.expense_category_id,
            expense_category_name=a.expense_category.name if a.expense_category else None,
            purchase_type_id=a.purchase_type_id,
            purchase_type_name=a.purchase_type.name if a.purchase_type else None,
            agreement_id=a.agreement_id,
            agreement_code=a.agreement.code if a.agreement else None,
            code_id=a.code_id,
            contractt_id=a.contractt_id,
            contract_code=a.contractt.code if a.contractt else None,
            pad_id=a.pad_id,
            pid_id=a.pid_id,
            pad_name=a.pid.pad if a.pid else None,
            contract_id=a.contract_id,
            rubro_id=a.rubro_id,
            status_id=a.status_id,
            general_cat_id=a.general_cat_id,
            kfw_id=a.kfw_id,
            person_id_implementer=a.person_id_implementer,
            person_id_executer=a.person_id_executer,
            vlr_id_typ_hiring=a.vlr_id_typ_hiring,
            vlr_id_sts_hiring=a.vlr_id_sts_hiring,
            vlr_id_typ_gnrl_ctg=a.vlr_id_typ_gnrl_ctg,
            trm=a.trm,
            initial_budget_cop=a.initial_budget_cop,
            initial_budget_usd=a.initial_budget_usd,
            initial_budget_eur=a.initial_budget_eur,
            final_budget_cop=a.final_budget_cop,
            final_budget_usd=a.final_budget_usd,
            final_budget_eur=a.final_budget_eur,
            appropriate=a.appropriate,
            appropriate_pending=a.appropriate_pending,
            fulfilled=a.fulfilled,
            unfulfilled=a.unfulfilled,
            paid_total_value=a.paid_total_value,
            unpaid_total_value=a.unpaid_total_value,
            apropiate_sicof=a.apropiate_sicof,
            execute_sicof=a.execute_sicof,
            acquisition_detail=a.acquisition_detail,
            detail=a.detail,
            code=a.code,
            code_siva=a.code_siva,
            observations=a.observations,
            cod_siva_contrato=a.cod_siva_contrato,
            cod_siva_acuerdo=a.cod_siva_acuerdo,
            version_creation=a.version_creation,
            version_update=a.version_update,
            created_at=a.created_at,
            updated_at=a.updated_at,
        )
        for a in acquisitions
    ]


def get_acquisition_by_id(id: int, db: Session) -> AcquisitionsBase | None:
    a = AcquisitionsRepository.get_acquisition_by_id(id, db)
    if not a:
        return None
    return AcquisitionsBase(
        id=int(a.id),
        process_number=a.process_number,
        type=a.type,
        description=a.description,
        numero_contrato_temporal=a.numero_contrato_temporal,
        status=a.status,
        contracts_qty=a.contracts_qty,
        activity_id=a.activity_id,
        activity_code=a.activity.code if a.activity else None,
        activity_description=a.activity.description if a.activity else None,
        expense_category_id=a.expense_category_id,
        expense_category_name=a.expense_category.name if a.expense_category else None,
        purchase_type_id=a.purchase_type_id,
        purchase_type_name=a.purchase_type.name if a.purchase_type else None,
        agreement_id=a.agreement_id,
        agreement_code=a.agreement.code if a.agreement else None,
        code_id=a.code_id,
        contractt_id=a.contractt_id,
        contract_code=a.contractt.code if a.contractt else None,
        pad_id=a.pad_id,
        pid_id=a.pid_id,
        pad_name=a.pid.pad if a.pid else None,
        contract_id=a.contract_id,
        rubro_id=a.rubro_id,
        status_id=a.status_id,
        general_cat_id=a.general_cat_id,
        kfw_id=a.kfw_id,
        person_id_implementer=a.person_id_implementer,
        person_id_executer=a.person_id_executer,
        vlr_id_typ_hiring=a.vlr_id_typ_hiring,
        vlr_id_sts_hiring=a.vlr_id_sts_hiring,
        vlr_id_typ_gnrl_ctg=a.vlr_id_typ_gnrl_ctg,
        trm=a.trm,
        initial_budget_cop=a.initial_budget_cop,
        initial_budget_usd=a.initial_budget_usd,
        initial_budget_eur=a.initial_budget_eur,
        final_budget_cop=a.final_budget_cop,
        final_budget_usd=a.final_budget_usd,
        final_budget_eur=a.final_budget_eur,
        appropriate=a.appropriate,
        appropriate_pending=a.appropriate_pending,
        fulfilled=a.fulfilled,
        unfulfilled=a.unfulfilled,
        paid_total_value=a.paid_total_value,
        unpaid_total_value=a.unpaid_total_value,
        apropiate_sicof=a.apropiate_sicof,
        execute_sicof=a.execute_sicof,
        acquisition_detail=a.acquisition_detail,
        detail=a.detail,
        code=a.code,
        code_siva=a.code_siva,
        observations=a.observations,
        cod_siva_contrato=a.cod_siva_contrato,
        cod_siva_acuerdo=a.cod_siva_acuerdo,
        version_creation=a.version_creation,
        version_update=a.version_update,
        created_at=a.created_at,
        updated_at=a.updated_at,
    )


def create_acquisition(acquisition: AcquisitionsCreate, db: Session, usuario_guid: str) -> ResponseRequest:
    respuesta = ResponseRequest(solicitud_exitosa=True)
    try:
        usuario = UsuariosRepository.obtener_por_guid_msft(usuario_guid.strip(), db)
        if not usuario:
            raise Exception("Usuario no encontrado")

        if not acquisition.process_number or not acquisition.type or not acquisition.activity_id \
           or not acquisition.expense_category_id or not acquisition.purchase_type_id:
            return ResponseRequest(
                solicitud_exitosa=False,
                mensaje='process_number, type, activity_id, expense_category_id y purchase_type_id son obligatorios'
            )

        nueva_adquisicion = AcquisitionsEntity()
        nueva_adquisicion.process_number = acquisition.process_number
        nueva_adquisicion.type = acquisition.type
        nueva_adquisicion.description = acquisition.description
        nueva_adquisicion.numero_contrato_temporal = acquisition.numero_contrato_temporal
        nueva_adquisicion.status = acquisition.status
        nueva_adquisicion.contracts_qty = acquisition.contracts_qty
        nueva_adquisicion.activity_id = acquisition.activity_id
        nueva_adquisicion.expense_category_id = acquisition.expense_category_id
        nueva_adquisicion.purchase_type_id = acquisition.purchase_type_id
        nueva_adquisicion.agreement_id = acquisition.agreement_id
        nueva_adquisicion.code_id = acquisition.code_id
        nueva_adquisicion.contractt_id = acquisition.contractt_id
        nueva_adquisicion.pad_id = acquisition.pad_id
        nueva_adquisicion.pid_id = acquisition.pid_id
        nueva_adquisicion.rubro_id = acquisition.rubro_id
        nueva_adquisicion.status_id = acquisition.status_id
        nueva_adquisicion.general_cat_id = acquisition.general_cat_id
        nueva_adquisicion.kfw_id = acquisition.kfw_id
        nueva_adquisicion.person_id_implementer = acquisition.person_id_implementer
        nueva_adquisicion.person_id_executer = acquisition.person_id_executer
        nueva_adquisicion.trm = acquisition.trm
        nueva_adquisicion.initial_budget_cop = acquisition.initial_budget_cop
        nueva_adquisicion.initial_budget_usd = acquisition.initial_budget_usd
        nueva_adquisicion.initial_budget_eur = acquisition.initial_budget_eur
        nueva_adquisicion.final_budget_cop = acquisition.final_budget_cop
        nueva_adquisicion.final_budget_usd = acquisition.final_budget_usd
        nueva_adquisicion.final_budget_eur = acquisition.final_budget_eur
        nueva_adquisicion.appropriate = acquisition.appropriate
        nueva_adquisicion.appropriate_pending = acquisition.appropriate_pending
        nueva_adquisicion.fulfilled = acquisition.fulfilled
        nueva_adquisicion.unfulfilled = acquisition.unfulfilled
        nueva_adquisicion.detail = acquisition.detail
        nueva_adquisicion.code = acquisition.code
        nueva_adquisicion.code_siva = acquisition.code_siva
        nueva_adquisicion.observations = acquisition.observations
        nueva_adquisicion.cod_siva_contrato = acquisition.cod_siva_contrato
        nueva_adquisicion.cod_siva_acuerdo = acquisition.cod_siva_acuerdo
        nueva_adquisicion.created_at = datetime.now()
        nueva_adquisicion.updated_at = datetime.now()

        nueva_adquisicion = AcquisitionsRepository.create_acquisition(nueva_adquisicion, db)

        respuesta.identity = nueva_adquisicion.id
        respuesta.mensaje = "Adquisición creada exitosamente"
        return respuesta

    except Exception as e:
        logging.error(f"Error al crear adquisición: {e}")
        db.rollback()
        return ResponseRequest(
            solicitud_exitosa=False,
            mensaje=str(e)
        )


def list_acquisitions_sp(
    db: Session,
    page: int = 1,
    filtro: str = "",
    pid: int = -1,
    actividad: int = -1,
    procesos: list[str] | None = None,
    rubros: list[str] | None = None,
    rubros_cortos: list[str] | None = None,
    actividad_codigo: str | None = None,   
) -> list[AcquisitionListSP]:
    try:
        return AcquisitionsRepository.list_acquisitions_sp(
            db, page, filtro, pid, actividad, procesos, rubros, rubros_cortos, actividad_codigo  
        )
    except Exception as e:
        logging.error(f"Failed to list acquisitions: {str(e)}")
        raise PruebaNotFoundError(str(e))


def update_acquisition(id: int, payload: AcquisitionsCreate, db: Session, usuario_guid: str) -> ResponseRequest:
    try:
        usuario = UsuariosRepository.obtener_por_guid_msft(usuario_guid.strip(), db)
        if not usuario:
            raise Exception("Usuario no encontrado")

        registro = AcquisitionsRepository.get_acquisition_by_id(id, db)
        if not registro:
            return ResponseRequest(solicitud_exitosa=False, mensaje='Adquisición no encontrada')

        registro.process_number = payload.process_number
        registro.type = payload.type
        registro.description = payload.description
        registro.numero_contrato_temporal = payload.numero_contrato_temporal
        registro.status = payload.status
        registro.contracts_qty = payload.contracts_qty
        registro.activity_id = payload.activity_id
        registro.expense_category_id = payload.expense_category_id
        registro.purchase_type_id = payload.purchase_type_id
        registro.agreement_id = payload.agreement_id
        registro.code_id = payload.code_id
        registro.contractt_id = payload.contractt_id
        registro.pad_id = payload.pad_id
        registro.pid_id = payload.pid_id
        registro.rubro_id = payload.rubro_id
        registro.status_id = payload.status_id
        registro.general_cat_id = payload.general_cat_id
        registro.kfw_id = payload.kfw_id
        registro.person_id_implementer = payload.person_id_implementer
        registro.person_id_executer = payload.person_id_executer
        registro.trm = payload.trm
        registro.initial_budget_cop = payload.initial_budget_cop
        registro.initial_budget_usd = payload.initial_budget_usd
        registro.initial_budget_eur = payload.initial_budget_eur
        registro.final_budget_cop = payload.final_budget_cop
        registro.final_budget_usd = payload.final_budget_usd
        registro.final_budget_eur = payload.final_budget_eur
        registro.appropriate = payload.appropriate
        registro.appropriate_pending = payload.appropriate_pending
        registro.fulfilled = payload.fulfilled
        registro.unfulfilled = payload.unfulfilled
        registro.detail = payload.detail
        registro.code = payload.code
        registro.code_siva = payload.code_siva
        registro.observations = payload.observations
        registro.cod_siva_contrato = payload.cod_siva_contrato
        registro.cod_siva_acuerdo = payload.cod_siva_acuerdo
        registro.updated_at = datetime.now()

        AcquisitionsRepository.update_acquisition(registro, db)

        return ResponseRequest(solicitud_exitosa=True, mensaje='Adquisición actualizada exitosamente', identity=registro.id)
    except Exception as e:
        db.rollback()
        logging.error(f"Error al actualizar adquisición: {e}")
        return ResponseRequest(solicitud_exitosa=False, mensaje=str(e))


def delete_acquisition(id: int, db: Session) -> ResponseRequest:
    try:
        registro = AcquisitionsRepository.get_acquisition_by_id(id, db)
        if not registro:
            return ResponseRequest(solicitud_exitosa=False, mensaje='Adquisición no encontrada')

        if AcquisitionsRepository.has_dependencies(id, db):
            return ResponseRequest(
                solicitud_exitosa=False,
                mensaje='No se puede eliminar: tiene implementadoras, contratos o notas asociadas'
            )

        AcquisitionsRepository.delete_acquisition(registro, db)
        return ResponseRequest(solicitud_exitosa=True, mensaje='Adquisición eliminada exitosamente', identity=id)
    except Exception as e:
        db.rollback()
        logging.error(f"Error al eliminar adquisición: {e}")
        return ResponseRequest(solicitud_exitosa=False, mensaje=str(e))