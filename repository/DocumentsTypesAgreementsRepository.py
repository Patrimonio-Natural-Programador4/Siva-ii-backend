import logging
from sqlalchemy.orm import Session
from entity.documents_types_agreements import DocumentsTypesAgreements
from exceptions import PruebaCreationError, PruebaNotFoundError


def listar(db: Session) -> list[DocumentsTypesAgreements]:
    try:
        return db.query(DocumentsTypesAgreements).order_by(DocumentsTypesAgreements.id.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list DocumentsTypesAgreements: {str(e)}")
        raise PruebaNotFoundError(str(e))


def crear_Tipos_Doc_Acu(doc_types_agreements: DocumentsTypesAgreements, db: Session) -> DocumentsTypesAgreements:
    try:
        db.add(doc_types_agreements)
        db.commit()
        db.refresh(doc_types_agreements)
        return doc_types_agreements
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create DocumentsTypesAgreements: {str(e)}")
        raise PruebaCreationError(str(e))
