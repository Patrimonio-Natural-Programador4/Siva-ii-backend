import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from dto.DisbursementDTO import DisbursementBase, DisbursementCreateBase
from dto.ResponseRequest import ResponseRequest
from entity.disbursement import Disbursement as DisbursementEntity
from repository import DisbursementRepository
from repository import DisbursementStateRepository
from exceptions import PruebaNotFoundError


def list_disbursement(db: Session) -> list[DisbursementBase]:
    disbursements = DisbursementRepository.list_disbursement(db)
    return [
        DisbursementBase(
            id=int(d.id),
            created_at=d.created_at,
            updated_at=d.updated_at,
            value=d.value,
            scheduled_date=d.scheduled_date,
            request_date=d.request_date,
            validation_date=d.validation_date,
            approval_date=d.approval_date,
            disbursement_date=d.disbursement_date,
            number_disbursement=d.number_disbursement,
            documento_soporte=d.documento_soporte,
            observations=d.observations,
            state_id=d.state_id,
            agreement_id=d.agreement_id,
            previous_studies_id=d.previous_studies_id,
            disbursement_state=d.disbursement_state.name if d.disbursement_state else None,
            disbursement_state_color=d.disbursement_state.color if d.disbursement_state else None,
            agreement=d.agreement.name if d.agreement else None,
            previous_study=d.previous_study.code if d.previous_study else None,
        )
        for d in disbursements
    ]


def get_disbursement_by_id(id: int, db: Session) -> DisbursementBase | None:
    d = DisbursementRepository.get_disbursement_by_id(id, db)
    if not d:
        return None
    return DisbursementBase(
        id=int(d.id),
        created_at=d.created_at,
        updated_at=d.updated_at,
        value=d.value,
        scheduled_date=d.scheduled_date,
        request_date=d.request_date,
        validation_date=d.validation_date,
        approval_date=d.approval_date,
        disbursement_date=d.disbursement_date,
        number_disbursement=d.number_disbursement,
        documento_soporte=d.documento_soporte,
        observations=d.observations,
        state_id=d.state_id,
        agreement_id=d.agreement_id,
        previous_studies_id=d.previous_studies_id,
        disbursement_state=d.disbursement_state.name if d.disbursement_state else None,
        disbursement_state_color=d.disbursement_state.color if d.disbursement_state else None,
        agreement=d.agreement.name if d.agreement else None,
        previous_study=d.previous_study.code if d.previous_study else None,
    )


def list_disbursement_by_agreement(agreement_id: int, db: Session) -> list[DisbursementBase]:
    try:
        disbursements = DisbursementRepository.get_disbursement_by_agreement(agreement_id, db)
        return [
            DisbursementBase(
                id=int(d.id),
                created_at=d.created_at,
                updated_at=d.updated_at,
                value=d.value,
                scheduled_date=d.scheduled_date,
                request_date=d.request_date,
                validation_date=d.validation_date,
                approval_date=d.approval_date,
                disbursement_date=d.disbursement_date,
                number_disbursement=d.number_disbursement,
                documento_soporte=d.documento_soporte,
                observations=d.observations,
                state_id=d.state_id,
                agreement_id=d.agreement_id,
                previous_studies_id=d.previous_studies_id,
                disbursement_state=d.disbursement_state.name if d.disbursement_state else None,
                disbursement_state_color=d.disbursement_state.color if d.disbursement_state else None,
                agreement=d.agreement.name if d.agreement else None,
                previous_study=d.previous_study.code if d.previous_study else None,
            )
            for d in disbursements
        ]
    except Exception as e:
        logging.error(f"Failed to list disbursements by agreement: {str(e)}")
        raise PruebaNotFoundError(str(e))
    
    
def list_disbursement_by_previous_studies(previous_studies_id: int, db: Session) -> list[DisbursementBase]:
    try:
        disbursements = DisbursementRepository.get_disbursement_by_previous_studies(previous_studies_id, db)
        return [
            DisbursementBase(
                id=int(d.id),
                created_at=d.created_at,
                updated_at=d.updated_at,
                value=d.value,
                scheduled_date=d.scheduled_date,
                request_date=d.request_date,
                validation_date=d.validation_date,
                approval_date=d.approval_date,
                disbursement_date=d.disbursement_date,
                number_disbursement=d.number_disbursement,
                documento_soporte=d.documento_soporte,
                observations=d.observations,
                state_id=d.state_id,
                agreement_id=d.agreement_id,
                previous_studies_id=d.previous_studies_id,
                disbursement_state=d.disbursement_state.name if d.disbursement_state else None,
                disbursement_state_color=d.disbursement_state.color if d.disbursement_state else None,
                agreement=d.agreement.name if d.agreement else None,
                previous_study=d.previous_study.code if d.previous_study else None,
            )
            for d in disbursements
        ]
    except Exception as e:
        logging.error(f"Failed to list disbursements by previous studies: {str(e)}")
        raise PruebaNotFoundError(str(e))


def create_disbursement(payload: DisbursementCreateBase, db: Session) -> ResponseRequest:
    response = ResponseRequest(solicitud_exitosa=True)
    try:
        if payload.state_id is not None:
            state = DisbursementStateRepository.get_disbursement_state_by_id(payload.state_id, db)
            if not state:
                return ResponseRequest(mensaje='El estado indicado no existe', solicitud_exitosa=False)

        new_disbursement = DisbursementEntity()
        new_disbursement.created_at = datetime.now(timezone.utc)
        new_disbursement.value = payload.value
        new_disbursement.scheduled_date = payload.scheduled_date
        new_disbursement.request_date = payload.request_date
        new_disbursement.validation_date = payload.validation_date
        new_disbursement.approval_date = payload.approval_date
        new_disbursement.disbursement_date = payload.disbursement_date
        new_disbursement.number_disbursement = payload.number_disbursement
        new_disbursement.documento_soporte = payload.documento_soporte
        new_disbursement.observations = payload.observations
        new_disbursement.state_id = payload.state_id
        new_disbursement.agreement_id = payload.agreement_id
        new_disbursement.previous_studies_id = payload.previous_studies_id

        db.add(new_disbursement)
        db.commit()
        db.refresh(new_disbursement)

        response.identity = new_disbursement.id
        response.mensaje = 'Desembolso creado exitosamente'
        return response

    except Exception as e:
        logging.error(f"Error creating disbursement: {e}")
        db.rollback()
        return ResponseRequest(solicitud_exitosa=False, mensaje=str(e))


def update_disbursement(id: int, payload: DisbursementCreateBase, db: Session) -> ResponseRequest:
    try:
        record = db.query(DisbursementEntity).filter(DisbursementEntity.id == id).first()
        if not record:
            return ResponseRequest(solicitud_exitosa=False, mensaje='Desembolso no encontrado')

        if payload.state_id is not None:
            state = DisbursementStateRepository.get_disbursement_state_by_id(payload.state_id, db)
            if not state:
                return ResponseRequest(solicitud_exitosa=False, mensaje='El estado indicado no existe')

        record.updated_at = datetime.now()
        record.value = payload.value
        record.scheduled_date = payload.scheduled_date
        record.request_date = payload.request_date
        record.validation_date = payload.validation_date
        record.approval_date = payload.approval_date
        record.disbursement_date = payload.disbursement_date
        record.number_disbursement = payload.number_disbursement
        record.documento_soporte = payload.documento_soporte
        record.observations = payload.observations
        record.state_id = payload.state_id
        record.agreement_id = payload.agreement_id
        record.previous_studies_id = payload.previous_studies_id

        db.commit()
        db.refresh(record)

        return ResponseRequest(solicitud_exitosa=True, mensaje='Desembolso actualizado exitosamente', identity=record.id)
    except Exception as e:
        db.rollback()
        logging.error(f"Error updating disbursement: {e}")
        return ResponseRequest(solicitud_exitosa=False, mensaje=str(e))