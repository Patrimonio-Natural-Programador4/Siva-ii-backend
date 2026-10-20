import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from dto.AgreementsProductsDTO import AgreementsProductsBase, AgreementsProductsCreateBase
from dto.ResponseRequest import ResponseRequest
from entity.agreements_products import AgreementsProducts as AgreementsProductsEntity
from repository import AgreementsProductsRepository

from exceptions import PruebaNotFoundError


def list_agreements_products(db: Session) -> list[AgreementsProductsBase]:
    agreements_products = AgreementsProductsRepository.list_agreements_products(db)
    return [
        AgreementsProductsBase(
            id=int(p.id),
            product=p.product,
            code=p.code,
            quantity=p.quantity,
            value=p.value,
            unit_measure=p.unit_measure,
            shared_ei_one_drive=p.shared_ei_one_drive,
            observations=p.observations,
            expected_fulfillment_date=p.expected_fulfillment_date,
            delivery_date=p.delivery_date,
            request_date=p.request_date,
            validation_date=p.validation_date,
            approval_date=p.approval_date,
            created_at=p.created_at,
            updated_at=p.updated_at,
            id_agreement=p.id_agreement,
            state_id=p.state_id,
            id_product=p.id_product,
            id_duplicate_product=p.id_duplicate_product,
            previous_studies_id=p.previous_studies_id,
            agreement=p.agreement.code if p.agreement else None,
            product_state=p.product_state.name if p.product_state else None,
            product_state_color=p.product_state.color if p.product_state else None,
            previous_study=p.previous_study.code if p.previous_study else None,
        )
        for p in agreements_products
    ]


def get_agreements_products_by_id(id: int, db: Session) -> AgreementsProductsBase | None:
    p = AgreementsProductsRepository.get_agreements_products_by_id(id, db)
    if not p:
        return None
    return AgreementsProductsBase(
        id=int(p.id),
        product=p.product,
        code=p.code,
        quantity=p.quantity,
        value=p.value,
        unit_measure=p.unit_measure,
        shared_ei_one_drive=p.shared_ei_one_drive,
        observations=p.observations,
        expected_fulfillment_date=p.expected_fulfillment_date,
        delivery_date=p.delivery_date,
        request_date=p.request_date,
        validation_date=p.validation_date,
        approval_date=p.approval_date,
        created_at=p.created_at,
        updated_at=p.updated_at,
        id_agreement=p.id_agreement,
        state_id=p.state_id,
        id_product=p.id_product,
        id_duplicate_product=p.id_duplicate_product,
        previous_studies_id=p.previous_studies_id,
        agreement=p.agreement.code if p.agreement else None,
        product_state=p.product_state.name if p.product_state else None,
        product_state_color=p.product_state.color if p.product_state else None,
        previous_study=p.previous_study.code if p.previous_study else None,
    )


def list_agreements_products_by_agreement(agreement_id: int, db: Session) -> list[AgreementsProductsBase]:
    try:
        agreements_products = AgreementsProductsRepository.get_agreements_products_by_agreement(agreement_id, db)
        return [
            AgreementsProductsBase(
                id=int(p.id),
                product=p.product,
                code=p.code,
                quantity=p.quantity,
                value=p.value,
                unit_measure=p.unit_measure,
                shared_ei_one_drive=p.shared_ei_one_drive,
                observations=p.observations,
                expected_fulfillment_date=p.expected_fulfillment_date,
                delivery_date=p.delivery_date,
                request_date=p.request_date,
                validation_date=p.validation_date,
                approval_date=p.approval_date,
                created_at=p.created_at,
                updated_at=p.updated_at,
                id_agreement=p.id_agreement,
                state_id=p.state_id,
                id_product=p.id_product,
                id_duplicate_product=p.id_duplicate_product,
                previous_studies_id=p.previous_studies_id,
                agreement=p.agreement.code if p.agreement else None,
                product_state=p.product_state.name if p.product_state else None,
                product_state_color=p.product_state.color if p.product_state else None,
                previous_study=p.previous_study.code if p.previous_study else None,
            )
            for p in agreements_products
        ]
    except Exception as e:
        logging.error(f"Failed to list agreements products by agreement: {str(e)}")
        raise PruebaNotFoundError(str(e))
    
    
def list_agreements_products_by_previous_studies(previous_studies_id: int, db: Session) -> list[AgreementsProductsBase]:
    try:
        agreements_products  = AgreementsProductsRepository.get_agreements_products_by_previous_studies(previous_studies_id, db)
        return [
            AgreementsProductsBase(
                id=int(p.id),
                product=p.product,
                code=p.code,
                quantity=p.quantity,
                value=p.value,
                unit_measure=p.unit_measure,
                shared_ei_one_drive=p.shared_ei_one_drive,
                observations=p.observations,
                expected_fulfillment_date=p.expected_fulfillment_date,
                delivery_date=p.delivery_date,
                request_date=p.request_date,
                validation_date=p.validation_date,
                approval_date=p.approval_date,
                created_at=p.created_at,
                updated_at=p.updated_at,
                id_agreement=p.id_agreement,
                state_id=p.state_id,
                id_product=p.id_product,
                id_duplicate_product=p.id_duplicate_product,
                previous_studies_id=p.previous_studies_id,
                agreement=p.agreement.code if p.agreement else None,
                product_state=p.product_state.name if p.product_state else None,
                product_state_color=p.product_state.color if p.product_state else None,
                previous_study=p.previous_study.code if p.previous_study else None,
            )
            for p in agreements_products 
        ]
    except Exception as e:
        logging.error(f"Failed to list agreements products by previous studies: {str(e)}")
        raise PruebaNotFoundError(str(e))


def create_agreements_products(payload: AgreementsProductsCreateBase, db: Session) -> ResponseRequest:
    response = ResponseRequest(solicitud_exitosa=True)
    try:
        if payload.state_id is not None:
            state = AgreementsProductsRepository.get_agreements_products_by_id(payload.state_id, db)
            if not state:
                return ResponseRequest(mensaje='El estado indicado no existe', solicitud_exitosa=False)

        new_product = AgreementsProductsEntity()
        new_product.created_at = datetime.now()
        new_product.product = payload.product.strip()
        new_product.code = payload.code
        new_product.quantity = payload.quantity
        new_product.value = payload.value
        new_product.unit_measure = payload.unit_measure
        new_product.shared_ei_one_drive = payload.shared_ei_one_drive
        new_product.observations = payload.observations
        new_product.expected_fulfillment_date = payload.expected_fulfillment_date
        new_product.delivery_date = payload.delivery_date
        new_product.request_date = payload.request_date
        new_product.validation_date = payload.validation_date
        new_product.approval_date = payload.approval_date
        new_product.id_agreement = payload.id_agreement
        new_product.state_id = payload.state_id
        new_product.id_product = payload.id_product
        new_product.id_duplicate_product = payload.id_duplicate_product
        new_product.previous_studies_id = payload.previous_studies_id

        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        response.identity = new_product.id
        response.mensaje = 'Producto creado exitosamente'
        return response

    except Exception as e:
        logging.error(f"Error creating agreements products: {e}")
        db.rollback()
        return ResponseRequest(solicitud_exitosa=False, mensaje=str(e))


def update_agreements_products(id: int, payload: AgreementsProductsCreateBase, db: Session) -> ResponseRequest:
    try:
        record = AgreementsProductsRepository.get_agreements_products_by_id(id, db)
        if not record:
            return ResponseRequest(solicitud_exitosa=False, mensaje='Producto no encontrado')

        record.updated_at = datetime.now()
        record.product = payload.product.strip()
        record.code = payload.code
        record.quantity = payload.quantity
        record.value = payload.value
        record.unit_measure = payload.unit_measure
        record.shared_ei_one_drive = payload.shared_ei_one_drive
        record.observations = payload.observations
        record.expected_fulfillment_date = payload.expected_fulfillment_date
        record.delivery_date = payload.delivery_date
        record.request_date = payload.request_date
        record.validation_date = payload.validation_date
        record.approval_date = payload.approval_date
        record.id_agreement = payload.id_agreement
        record.state_id = payload.state_id
        record.id_product = payload.id_product
        record.id_duplicate_product = payload.id_duplicate_product
        record.previous_studies_id = payload.previous_studies_id

        AgreementsProductsRepository.update_agreements_products(record, db)

        return ResponseRequest(solicitud_exitosa=True, mensaje='Producto actualizado exitosamente', identity=record.id)
    except Exception as e:
        db.rollback()
        logging.error(f"Error updating agreements product: {e}")
        return ResponseRequest(solicitud_exitosa=False, mensaje=str(e))