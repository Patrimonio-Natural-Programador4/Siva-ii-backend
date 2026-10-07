from sqlalchemy.orm import Session
from entity.documents_types_travels import DocumentsTypesTravels
import logging

def listar_tipos_documentos_viaje(db: Session) -> list[DocumentsTypesTravels]:
    try:
        return db.query(DocumentsTypesTravels).order_by(DocumentsTypesTravels.document_category.asc()).all()
    except Exception as e:
        logging.error(f"Failed to fetch documents types travels: {str(e)}")
        raise
