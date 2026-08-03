import logging
import traceback
from sqlalchemy.orm import Session

from dto.DocumentsApprovalDTO import (
    DocumentsApprovalBase)
from dto.ResponseRequest import ResponseRequest
from entity.documents_approval import DocumentsApproval
from repository  import DocumentsApprovalRepository
from dto.DocumentsApprovalDTO import (
    DocumentsCreateBase)
from dto.DocumentsApprovalDTO import (
    DocumentsUpdateBase)

from dto.DocumentsApprovalDTO import (
    DocumentsApprovalListDTO,
)


def listar_documentos_aprobados(db: Session) -> list[DocumentsApprovalListDTO]:
    doc_aprobados = DocumentsApprovalRepository.listar_documentos_aprobacion(db)

    return [
        DocumentsApprovalListDTO(
            id=item["id"],
            documento=item["documento"],
            categoria=item["categoria"],
            programa=item["programa"],
         
        )
        for item in doc_aprobados
    ]


def crear_documento(payload: DocumentsCreateBase, db: Session) -> ResponseRequest:
    try:
        existente = DocumentsApprovalRepository.obtener_por_nombre(payload.documento or '', db)
        if existente:
            return ResponseRequest(mensaje='Ya existe un documento con ese nombre', solicitud_exitosa=False)

      
        nuevo = DocumentsApproval(
            approval_category_id=payload.approval_category_id,
            program_id=payload.program_id,
            name=payload.documento,
        )

        creado = DocumentsApprovalRepository.crear(nuevo, db)

        return ResponseRequest(
            mensaje='Documento creado exitosamente', 
            identity=int(creado.id), 
            solicitud_exitosa=True
        )
    except Exception as e:
        logging.error(f"Error creating program: {str(e)}")
        return ResponseRequest(
            mensaje='Error al crear el documento', 
            solicitud_exitosa=False
        )


def obtener_doc_por_id(id: int, db: Session) -> DocumentsApprovalBase | None:
    doc = DocumentsApprovalRepository.obtener_por_id(id, db)

    if not doc:
        return None

    return DocumentsApprovalBase(
        id= int(doc.id),
        documento=doc.name,
        approval_category_id=doc.approval_category_id,
        program_id=doc.program_id
    )

def editar_documento(id: int, payload: DocumentsUpdateBase, db: Session) -> ResponseRequest:
    try:
       
        documento_db = DocumentsApprovalRepository.obtener_por_id(id=id, db=db)
        if not documento_db:
            return ResponseRequest(mensaje='El documento a editar no existe', solicitud_exitosa=False)

        # Asignar los campos
        documento_db.approval_category_id = payload.approval_category_id
        documento_db.program_id = payload.program_id
        
        
        nombre_documento = getattr(payload, 'documento', None) or getattr(payload, 'name', None)
        documento_db.name = nombre_documento
        
        #Guardar cambios
        actualizado = DocumentsApprovalRepository.actualizar(document_approval=documento_db, db=db)
        
        return ResponseRequest(
            mensaje='Documento actualizado exitosamente', 
            identity=int(actualizado.id), 
            solicitud_exitosa=True
        )
        
    except Exception as e:
        logging.error(f"Error detallado en editar_documento: {traceback.format_exc()}")
        return ResponseRequest(
            mensaje='Error al actualizar el documento', 
            solicitud_exitosa=False
        )
        
       
  
        