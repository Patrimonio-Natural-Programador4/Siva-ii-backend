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

# obtiene el doc por template (nombre) para evitar duplicados
def obtener_por_template(template: str, db: Session) -> DocumentsTypesAgreements | None:
    try:
        return db.query(DocumentsTypesAgreements).filter(DocumentsTypesAgreements.template.ilike(template.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get program by template: {str(e)}")
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

#obtiene doc por id 

def obtener_Tipos_Doc_Acu_por_id(id:int, db:Session)-> DocumentsTypesAgreements:
    try:
        print("Buscando ID:", id)

        doc = db.query(DocumentsTypesAgreements)\
                .filter(DocumentsTypesAgreements.id == id)\
                .first()

        return doc

    except Exception as e:
        logging.error(f"Failed to find DocumentsTypesAgreements by id: {str(e)}")
        return None

def actualizar_Tipos_Doc_Acu(tipoDoc:DocumentsTypesAgreements, db:Session)-> DocumentsTypesAgreements:
    try:
        db.commit()
        db.refresh(tipoDoc)
        return tipoDoc
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create documentsTypesAgreement: {str(e)}  ")
        raise PruebaCreationError(str(e))
    