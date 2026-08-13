import logging
import traceback
from sqlalchemy.orm import Session
from exceptions import PruebaCreationError, PruebaNotFoundError
from dto.DocumentsTypesAgreements import DocumentsTypesAgreementsBase,DocumentsTypesAgreementsUpdateBase,DocumentsTypesAgreementsCreateBase
from repository import DocumentsTypesAgreementsRepository
from dto.ResponseRequest import ResponseRequest
from entity.documents_types_agreements import DocumentsTypesAgreements


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
            documents_approval=p.documents_approval.name if p.documents_approval else None,
        )
        for p in documentos
    ]
    
    
def crear_tipo_doc(payload: DocumentsTypesAgreementsBase, db: Session) -> ResponseRequest:
    try:
        existente = DocumentsTypesAgreementsRepository.obtener_por_template(payload.template or '', db)
        if existente:
            return ResponseRequest(mensaje='Ya existe un tipo de documento con ese nombre', solicitud_exitosa=False)
        nuevo = DocumentsTypesAgreements(
            is_required =payload.is_required,
            description=payload.description,
            number=payload.number,
            code=payload.code,
            template=payload.template,
            template_path =payload.template_path,
            is_active=payload.is_active,
            documents_approval_id=payload.documents_approval_id, 
        )
        creado = DocumentsTypesAgreementsRepository.crear_Tipos_Doc_Acu(nuevo, db)
        return ResponseRequest(
            mensaje='Tipo de documento creado exitosamente', 
            identity=int(creado.id), 
            solicitud_exitosa=True
        )
    except Exception as e:
        logging.error(f"Error creating program: {str(e)}")
        return ResponseRequest(
            mensaje='Error al crear el tipo de documento', 
            solicitud_exitosa=False
        )
    
def obtener_tipo_doc_acu_por_id(id: int, db: Session) -> DocumentsTypesAgreementsBase | None:
    doc = DocumentsTypesAgreementsRepository.obtener_Tipos_Doc_Acu_por_id(id, db)

    if not doc:
        return None

    return DocumentsTypesAgreementsBase(
    id=int(doc.id),
    is_required=doc.is_required,
    description=doc.description,
    number=doc.number,
    code=doc.code,
    template=doc.template,
    template_path=doc.template_path,
    is_active=doc.is_active,
    documents_approval=doc.documents_approval.name if  doc.documents_approval else None,
)
    
def editar_tipo_doc_acu(id: int, payload: DocumentsTypesAgreementsUpdateBase, db: Session) -> ResponseRequest:
    try:

        tipo_doc_acu_db = DocumentsTypesAgreementsRepository.obtener_Tipos_Doc_Acu_por_id(id, db)
        if not tipo_doc_acu_db:
            return ResponseRequest(mensaje='Tipo de documento no encontrado', solicitud_exitosa=False)

        template_nuevo = (payload.template or '').strip()
        if template_nuevo and template_nuevo.lower() != (tipo_doc_acu_db.template or '').lower():
            existente = DocumentsTypesAgreementsRepository.obtener_por_template(template_nuevo, db)
            if existente:
                return ResponseRequest(mensaje='Ya existe un tipo de documento con ese nombre de plantilla', solicitud_exitosa=False)

        tipo_doc_acu_db.is_required = payload.is_required
        tipo_doc_acu_db.description = payload.description
        tipo_doc_acu_db.number = payload.number
        tipo_doc_acu_db.code = payload.code
        tipo_doc_acu_db.template = template_nuevo
        tipo_doc_acu_db.template_path = payload.template_path
        tipo_doc_acu_db.is_active = payload.is_active
        tipo_doc_acu_db.documents_approval_id = payload.documents_approval_id

        actualizado = DocumentsTypesAgreementsRepository.actualizar_Tipos_Doc_Acu(tipo_doc_acu_db, db)
        return ResponseRequest(mensaje='Tipo de documento actualizado exitosamente', identity=id, solicitud_exitosa=True)

    except Exception as e:
        logging.error(f"Error updating tipo documento acuerdo: {str(e)}")
        return ResponseRequest(mensaje='Error al actualizar el tipo de documento', solicitud_exitosa=False)
        
    
    
    