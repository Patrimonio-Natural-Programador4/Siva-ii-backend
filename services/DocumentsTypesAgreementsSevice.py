import logging
from sqlalchemy.orm import Session

from dto.DocumentsTypesAgreements import DocumentsTypesAgreementsBase
from repository import DocumentsTypesAgreementsRepository


def listar(db: Session) -> list[DocumentsTypesAgreementsBase]:
    documentos = DocumentsTypesAgreementsRepository.listar(db)

    return [
        DocumentsTypesAgreementsBase(
            id=int(p.id),
            is_required=p.is_required,
            description=p.description,
            number=p.number,
            code=p.code,
            template=p.template,
            template_path=p.template_path,
            is_active=p.is_active,
            documents_approval_id=p.documents_approval_id,
        )
        for p in documentos
    ]
    
    
    