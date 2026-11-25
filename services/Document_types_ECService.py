import logging
from sqlalchemy.orm import Session

from dto.Document_types_ECDTO import Document_types_EC
from repository import Document_types_ECRepository


def list_document_types_ec(db: Session, ) -> Document_types_EC:
    result = Document_types_ECRepository.list_document_types_ec(db)
    return Document_types_EC(
        resultado=result.resultado,
    )
