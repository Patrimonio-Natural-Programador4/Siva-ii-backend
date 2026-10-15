import logging
from sqlalchemy.orm import Session

from dto.agreementDTO import AgreementsBase, AgreementsCreateBase
from dto.ResponseRequest import ResponseRequest
from entity.agreements import Agreements
from repository import AgreementRepository,UsuariosRepository
from datetime import datetime
from zoneinfo import ZoneInfo
from exceptions import PruebaNotFoundError


def listar(db: Session) -> list[AgreementsBase]:
    agreements = AgreementRepository.listar(db)
    return [
        AgreementsBase(
            id=int(a.id),
            name=a.name,
            code=a.code,
            local=a.local,
            description=a.description,
            value=a.value,
            is_currency_usd=a.is_currency_usd,
            year=a.year,
            request_date=a.request_date,
            finish_date=a.finish_date,
            signature_fpn=a.signature_fpn,
            signature_ei=a.signature_ei,
            file_date=a.file_date,
            policy_approval=a.policy_approval,
            signature_date=a.signature_date,
            time_limit=a.time_limit,
            policy_date=a.policy_date,
            liquidation_date=a.liquidation_date,
            final_date=a.final_date,
            agreement_id=a.agreement_id,
            agreement_stage_id=a.agreement_stage_id,
            marking=a.marking,
            priority=a.priority,
            notes=a.notes,
            is_valid=a.is_valid,
            observations=a.observations,
            products=a.products,
            created_at=a.created_at,
            updated_at=a.updated_at,
            alert=a.alert,
            liquidation_file_date=a.liquidation_file_date,
            finish_file_record_date=a.finish_file_record_date,
            general_remarks=a.general_remarks,
            email_notifications=a.email_notifications,
            executed_value=a.executed_value,
            financial_progress=a.financial_progress,
            summary=a.summary,
            total_value=a.total_value,
            financial_cutoff_date=a.financial_cutoff_date,
            value_executes_fpn=a.value_executes_fpn,
            value_executes_entity=a.value_executes_entity,
            counterpart_execution_progress=a.counterpart_execution_progress,
            ei_executed_value=a.ei_executed_value,
            fpn_executed_value=a.fpn_executed_value,
            total_value_executes_FPN=a.total_value_executes_FPN,
            total_value_executes_EI=a.total_value_executes_EI,
            last_report_date=a.last_report_date,
            contract_file_sharepoint=a.contract_file_sharepoint,
            shared_ei_one_drive=a.shared_ei_one_drive,
            shared_products_ei_one_drive=a.shared_products_ei_one_drive,
            village=a.village,
            hectares=a.hectares,
            beneficiaries=a.beneficiaries,
            advance_hectares=a.advance_hectares,
            advance_beneficiaries=a.advance_beneficiaries,
            hectares_beneficiaries_updated_at=a.hectares_beneficiaries_updated_at,
            have_aatis=a.have_aatis,
            aatis=a.aatis,
            councils=a.councils,
            resguard=a.resguard,
            municipality=a.municipality,
            department=a.department,
            legal_observations=a.legal_observations,
            acquisitions_observations=a.acquisitions_observations,
            uer_observations=a.uer_observations,
            agreement_origin_id= a.agreement_origin_id,
            agreement_origin_name = a.agreement_origin.name if a.agreement_origin else None,
            agreement_stage = a.agreement_stage.name if a.agreement_stage else None,
            agreement_type_id = a.agreement_type_id,
            agreement_type    = a.agreement_type.name if a.agreement_type else None,
            modality_id= a.modality_id,
            modality =  a.modality.name if a.modality else None,
            pillar_id= a.pillar_id,
            pillar =    a.pillar.name if a.pillar else None,
            program_id= a.program_id,
            program =    a.program.name if a.program else None,
            region_id = a.region_id,
            region =    a.region.name if a.region else None,
            precedents =  a.precedents,
            justification =  a.justification,
            scope =  a.scope,
        )
        for a in agreements
    ]


def obtener_por_id(id: int, db: Session) -> AgreementsBase | None:
    a= AgreementRepository.obtener_por_id(id, db)

    if not a:
        return None
    return        AgreementsBase(
                id=int(a.id),
                name=a.name,
                code=a.code,
                local=a.local,
                description=a.description,
                value=a.value,
                is_currency_usd=a.is_currency_usd,
                year=a.year,
                request_date=a.request_date,
                finish_date=a.finish_date,
                signature_fpn=a.signature_fpn,
                signature_ei=a.signature_ei,
                file_date=a.file_date,
                policy_approval=a.policy_approval,
                signature_date=a.signature_date,
                time_limit=a.time_limit,
                policy_date=a.policy_date,
                liquidation_date=a.liquidation_date,
                final_date=a.final_date,
                agreement_id=a.agreement_id,
            
                marking=a.marking,
                priority=a.priority,
                notes=a.notes,
                is_valid=a.is_valid,
                observations=a.observations,
                products=a.products,
                created_at=a.created_at,
                updated_at=a.updated_at,
                alert=a.alert,
                liquidation_file_date=a.liquidation_file_date,
                finish_file_record_date=a.finish_file_record_date,
                general_remarks=a.general_remarks,
                email_notifications=a.email_notifications,
                executed_value=a.executed_value,
                financial_progress=a.financial_progress,
                summary=a.summary,
                total_value=a.total_value,
                financial_cutoff_date=a.financial_cutoff_date,
                value_executes_fpn=a.value_executes_fpn,
                value_executes_entity=a.value_executes_entity,
                counterpart_execution_progress=a.counterpart_execution_progress,
                ei_executed_value=a.ei_executed_value,
                fpn_executed_value=a.fpn_executed_value,
                total_value_executes_FPN=a.total_value_executes_FPN,
                total_value_executes_EI=a.total_value_executes_EI,
                last_report_date=a.last_report_date,
                contract_file_sharepoint=a.contract_file_sharepoint,
                shared_ei_one_drive=a.shared_ei_one_drive,
                shared_products_ei_one_drive=a.shared_products_ei_one_drive,
                village=a.village,
                hectares=a.hectares,
                beneficiaries=a.beneficiaries,
                advance_hectares=a.advance_hectares,
                advance_beneficiaries=a.advance_beneficiaries,
                hectares_beneficiaries_updated_at=a.hectares_beneficiaries_updated_at,
                have_aatis=a.have_aatis,
                aatis=a.aatis,
                councils=a.councils,
                resguard=a.resguard,
                municipality=a.municipality,
                department=a.department,
                legal_observations=a.legal_observations,
                acquisitions_observations=a.acquisitions_observations,
                uer_observations=a.uer_observations,
                agreement_origin_id= a.agreement_origin_id,
                agreement_origin_name =a.agreement_origin.name if a.agreement_origin else None,
        
                agreement_stage_id=a.agreement_stage_id,
                agreement_stage = a.agreement_stage.name if a.agreement_stage else None,
                agreement_type_id = a.agreement_type_id,
                agreement_type    = a.agreement_type.name if a.agreement_type else None,
                modality_id= a.modality_id,
                modality =  a.modality.name if a.modality else None,
                pillar_id= a.pillar_id,
                pillar =    a.pillar.name if a.pillar else None,
                program_id= a.program_id,
                program =    a.program.name if a.program else None,
          
                region_id = a.region_id,
                region =    a.region.name if a.region else None,
            
                precedents =  a.precedents,
                justification =  a.justification,
                scope =  a.scope,
                
                prevou_study_id = a.prevou_study_id,
                previous_study =    a.previous_study.precedents if a.previous_study else None,
                 
            )
    
        
def crear_agreement(payload: AgreementsCreateBase, db: Session) -> ResponseRequest:
    try:
        
        #print(" payload ", payload)
        # Validar campos obligatorios (NOT NULL en la tabla)
        """
        obligatorios = {
            'agreement_stage_id': payload.agreement_stage_id,
            'agreement_type_id': payload.agreement_type_id,
            'agreement_origin_id': payload.agreement_origin_id,
            'program_id': payload.program_id,
        }
        faltantes = [campo for campo, valor in obligatorios.items() if valor is None]
        if faltantes:
            return ResponseRequest(
                mensaje=f'Campos obligatorios faltantes: {", ".join(faltantes)}',
                solicitud_exitosa=False
            )
        """
        # 
        code = (payload.code or '').strip()
        if code:
            existente = AgreementRepository.obtener_por_code(code, db)
            if existente:
                return ResponseRequest(mensaje='Ya existe un acuerdo con ese código', solicitud_exitosa=False)
       
        nuevo = Agreements(
            name=(payload.name or '').strip(),
            code=code or None,
            local=payload.local,
            description=payload.description,
            value=payload.value,
            is_currency_usd=payload.is_currency_usd or False,
            year=payload.year,
            request_date=payload.request_date,
            finish_date=payload.finish_date,
            signature_fpn=payload.signature_fpn,
            signature_ei=payload.signature_ei,
            file_date=payload.file_date,
            policy_approval=payload.policy_approval or False,
            signature_date=payload.signature_date,
            time_limit=payload.time_limit,
            policy_date=payload.policy_date,
            liquidation_date=payload.liquidation_date,
            final_date=payload.final_date,

            #  foráneas
            agreement_id=payload.agreement_id,
            program_id=payload.program_id,
            pillar_id=payload.pillar_id,
            agreement_type_id=payload.agreement_type_id,
            agreement_stage_id=payload.agreement_stage_id,   # <-- faltaba
            agreement_origin_id=payload.agreement_origin_id,
            region_id=payload.region_id,
            modality_id=payload.modality_id,

            marking=payload.marking,
            priority=payload.priority,
            notes=payload.notes,
            is_valid=payload.is_valid,
            observations=payload.observations,
            products=payload.products,
            alert=payload.alert,
            liquidation_file_date=payload.liquidation_file_date,
            finish_file_record_date=payload.finish_file_record_date,
            general_remarks=payload.general_remarks,
            email_notifications=payload.email_notifications,
            executed_value=payload.executed_value,
            financial_progress=payload.financial_progress,
            summary=payload.summary,
            total_value=payload.total_value,
            financial_cutoff_date=payload.financial_cutoff_date,
            value_executes_fpn=payload.value_executes_fpn,
            value_executes_entity=payload.value_executes_entity,
            counterpart_execution_progress=payload.counterpart_execution_progress,
            ei_executed_value=payload.ei_executed_value,
            fpn_executed_value=payload.fpn_executed_value,
            total_value_executes_FPN=payload.total_value_executes_FPN,
            total_value_executes_EI=payload.total_value_executes_EI,
            last_report_date=payload.last_report_date,
            contract_file_sharepoint=payload.contract_file_sharepoint,
            shared_ei_one_drive=payload.shared_ei_one_drive,
            shared_products_ei_one_drive=payload.shared_products_ei_one_drive,
            village=payload.village,
            hectares=payload.hectares,
            beneficiaries=payload.beneficiaries,
            advance_hectares=payload.advance_hectares,
            advance_beneficiaries=payload.advance_beneficiaries,
            hectares_beneficiaries_updated_at=payload.hectares_beneficiaries_updated_at,
            have_aatis=payload.have_aatis,
            aatis=payload.aatis,
            councils=payload.councils,
            resguard=payload.resguard,
            municipality=payload.municipality,
            department=payload.department,
            legal_observations=payload.legal_observations,
            acquisitions_observations=payload.acquisitions_observations,
            uer_observations=payload.uer_observations,
            
            #campos E.P
            precedents=payload.precedents,
            justification=payload.justification,
            scope=payload.scope,
            prevou_study_id = payload.prevou_study_id,
            created_at=datetime.now(ZoneInfo("America/Bogota")).replace(tzinfo=None),
            
        )

        creado = AgreementRepository.crear_agreement(nuevo, db)
        return ResponseRequest(
            mensaje='Acuerdo creado exitosamente',
            identity=int(creado.id),
            solicitud_exitosa=True
        )

    except Exception as e:
        logging.error(f"Error creating agreement: {str(e)}")
        return ResponseRequest(mensaje='Error al crear el acuerdo', solicitud_exitosa=False)
    
def actualizar(guid: str, payload: AgreementsCreateBase, db: Session, usuario_guid: str) -> ResponseRequest:
    try:
        usuario = UsuariosRepository.obtener_por_guid_msft(usuario_guid.strip(), db)
        if not usuario:
            raise PruebaNotFoundError("Usuario no encontrado")

        acuerdo = AgreementRepository.obtener_por_uuid(guid, db)
        if not acuerdo:
            return ResponseRequest(solicitud_exitosa=False, mensaje='Acuerdo no encontrado')

        datos = payload.model_dump(exclude_unset=True)  # Pydantic v2 (en v1: payload.dict(exclude_unset=True))
        for campo, valor in datos.items():
            if hasattr(acuerdo, campo):
                setattr(acuerdo, campo, valor)

        db.commit()
        db.refresh(acuerdo)

        return ResponseRequest(solicitud_exitosa=True, mensaje='Acuerdo actualizado exitosamente', identity=acuerdo.id)
    except Exception as e:
        db.rollback()
        logging.error(f"Error al actualizar acuerdo: {e}")
        return ResponseRequest(solicitud_exitosa=False, mensaje=str(e)) 

"""
def actualizar(guid: str, payload: AgreementsCreateBase, db: Session, usuario_guid: str) -> ResponseRequest:
    try:
        usuario = UsuariosRepository.obtener_por_guid_msft(usuario_guid.strip(), db)
        if not usuario:
            raise PruebaNotFoundError("Usuario no encontrado")

        acuerdo = AgreementRepository.obtener_por_uuid(guid, db)
        if not acuerdo:
            return ResponseRequest(solicitud_exitosa=False, mensaje='Acuerdo previo no encontrado')

        acuerdo.name = payload.name,
     
        acuerdo.code = payload.code ,
        acuerdo.local = payload.local,
        acuerdo.description = payload.description,
        acuerdo.value = payload.value,
        acuerdo.is_currency_usd = payload.is_currency_usd,
        acuerdo.year = payload.year,
        acuerdo.request_date = payload.request_date,
        acuerdo.finish_date = payload.finish_date,
        acuerdo.signature_fpn = payload.signature_fpn,
        acuerdo.signature_ei = payload.signature_ei,
        acuerdo.file_date = payload.file_date,
        #acuerdo.policy_approval = payload.policy_approval,
        acuerdo.signature_date = payload.signature_date,
        acuerdo.time_limit = payload.time_limit,
        acuerdo.policy_date = payload.policy_date,
        acuerdo.liquidation_date = payload.liquidation_date,
        acuerdo.final_date = payload.final_date,

        # foráneas
        acuerdo.agreement_id = payload.agreement_id,
        acuerdo.program_id = payload.program_id,
        acuerdo.pillar_id = payload.pillar_id,
        acuerdo.agreement_type_id = payload.agreement_type_id,
        acuerdo.agreement_stage_id = payload.agreement_stage_id,  # <-- faltaba
        acuerdo.agreement_origin_id = payload.agreement_origin_id,
        acuerdo.region_id = payload.region_id,
        acuerdo.modality_id = payload.modality_id,

        acuerdo.marking = payload.marking,
        acuerdo.priority = payload.priority,
        acuerdo.notes = payload.notes,
        #acuerdo.is_valid = payload.is_valid,
        acuerdo.observations = payload.observations,
        acuerdo.products = payload.products,
        acuerdo.alert = payload.alert,
        acuerdo.liquidation_file_date = payload.liquidation_file_date,
        acuerdo.finish_file_record_date = payload.finish_file_record_date,
        acuerdo.general_remarks = payload.general_remarks,
        acuerdo.email_notifications = payload.email_notifications,
        acuerdo.executed_value = payload.executed_value,
        acuerdo.financial_progress = payload.financial_progress,
        acuerdo.summary = payload.summary,
        acuerdo.total_value = payload.total_value,
        acuerdo.financial_cutoff_date = payload.financial_cutoff_date,
        acuerdo.value_executes_fpn = payload.value_executes_fpn,
        acuerdo.value_executes_entity = payload.value_executes_entity,
        acuerdo.counterpart_execution_progress = payload.counterpart_execution_progress,
        acuerdo.ei_executed_value = payload.ei_executed_value,
        acuerdo.fpn_executed_value = payload.fpn_executed_value,
        acuerdo.total_value_executes_FPN = payload.total_value_executes_FPN,
        acuerdo.total_value_executes_EI = payload.total_value_executes_EI,
        acuerdo.last_report_date = payload.last_report_date,
        acuerdo.contract_file_sharepoint = payload.contract_file_sharepoint,
        acuerdo.shared_ei_one_drive = payload.shared_ei_one_drive,
        acuerdo.shared_products_ei_one_drive = payload.shared_products_ei_one_drive,
        acuerdo.village = payload.village,
        acuerdo.hectares = payload.hectares,
        acuerdo.beneficiaries = payload.beneficiaries,
        acuerdo.advance_hectares = payload.advance_hectares,
        acuerdo.advance_beneficiaries = payload.advance_beneficiaries,
        acuerdo.hectares_beneficiaries_updated_at = payload.hectares_beneficiaries_updated_at,
        acuerdo.have_aatis = payload.have_aatis,
        acuerdo.aatis = payload.aatis,
        acuerdo.councils = payload.councils,
        acuerdo.resguard = payload.resguard,
        acuerdo.municipality = payload.municipality,
        acuerdo.department = payload.department,
        acuerdo.legal_observations = payload.legal_observations,
        acuerdo.acquisitions_observations = payload.acquisitions_observations,
        acuerdo.uer_observations = payload.uer_observations,

        # campos E.P
        acuerdo.precedents = payload.precedents,
        acuerdo.justification = payload.justification,
        acuerdo.scope = payload.scope,
        acuerdo.prevou_study_id = payload.prevou_study_id,
    

        db.commit()
        db.refresh(acuerdo)

        return ResponseRequest(solicitud_exitosa=True, mensaje='Acuerdo  actualizado exitosamente', identity=acuerdo.id)
    except Exception as e:
        db.rollback()
        logging.error(f"Error al actualizar estudio previo: {e}")
        return ResponseRequest(solicitud_exitosa=False, mensaje=str(e))
"""
def obtener_por_uuid(uuid: str, db: Session) -> AgreementsBase | None:
    a= AgreementRepository.obtener_por_uuid(uuid, db)

    if not a:
        return None
    return        AgreementsBase(
                id=int(a.id),
                name=a.name,
                codee=a.code,
                local=a.local,
                description=a.description,
                value=a.value,
                is_currency_usd=a.is_currency_usd,
                year=a.year,
                request_date=a.request_date,
                finish_date=a.finish_date,
                signature_fpn=a.signature_fpn,
                signature_ei=a.signature_ei,
                file_date=a.file_date,
                policy_approval=a.policy_approval,
                signature_date=a.signature_date,
                time_limit=a.time_limit,
                policy_date=a.policy_date,
                liquidation_date=a.liquidation_date,
                final_date=a.final_date,
                agreement_id=a.agreement_id,
            
                marking=a.marking,
                priority=a.priority,
                notes=a.notes,
                is_valid=a.is_valid,
                observations=a.observations,
                products=a.products,
                created_at=a.created_at,
                updated_at=a.updated_at,
                alert=a.alert,
                liquidation_file_date=a.liquidation_file_date,
                finish_file_record_date=a.finish_file_record_date,
                general_remarks=a.general_remarks,
                email_notifications=a.email_notifications,
                executed_value=a.executed_value,
                financial_progress=a.financial_progress,
                summary=a.summary,
                total_value=a.total_value,
                financial_cutoff_date=a.financial_cutoff_date,
                value_executes_fpn=a.value_executes_fpn,
                value_executes_entity=a.value_executes_entity,
                counterpart_execution_progress=a.counterpart_execution_progress,
                ei_executed_value=a.ei_executed_value,
                fpn_executed_value=a.fpn_executed_value,
                total_value_executes_FPN=a.total_value_executes_FPN,
                total_value_executes_EI=a.total_value_executes_EI,
                last_report_date=a.last_report_date,
                contract_file_sharepoint=a.contract_file_sharepoint,
                shared_ei_one_drive=a.shared_ei_one_drive,
                shared_products_ei_one_drive=a.shared_products_ei_one_drive,
                village=a.village,
                hectares=a.hectares,
                beneficiaries=a.beneficiaries,
                advance_hectares=a.advance_hectares,
                advance_beneficiaries=a.advance_beneficiaries,
                hectares_beneficiaries_updated_at=a.hectares_beneficiaries_updated_at,
                have_aatis=a.have_aatis,
                aatis=a.aatis,
                councils=a.councils,
                resguard=a.resguard,
                municipality=a.municipality,
                department=a.department,
                legal_observations=a.legal_observations,
                acquisitions_observations=a.acquisitions_observations,
                uer_observations=a.uer_observations,
                agreement_origin_id= a.agreement_origin_id,
                agreement_origin_name =a.agreement_origin.name if a.agreement_origin else None,
        
                agreement_stage_id=a.agreement_stage_id,
                agreement_stage = a.agreement_stage.name if a.agreement_stage else None,
                agreement_type_id = a.agreement_type_id,
                agreement_type    = a.agreement_type.name if a.agreement_type else None,
                modality_id= a.modality_id,
                modality =  a.modality.name if a.modality else None,
                pillar_id= a.pillar_id,
                pillar =    a.pillar.name if a.pillar else None,
                program_id= a.program_id,
                program =    a.program.name if a.program else None,
          
                region_id = a.region_id,
                region =    a.region.name if a.region else None,
            
                precedents =  a.precedents,
                justification =  a.justification,
                scope =  a.scope,
                
                
                prevou_study_id = a.prevou_study_id,
                previous_study =    a.previous_study.precedents if a.previous_study else None,
                 
            )