from sqlalchemy.orm import Session
from repository import DocumentsTypesTravelsRepository

# No confundir con el listado de documentos de los usuarios
# Este es para los documentos que se suben a los viajes

def listar_tipos_documentos_viaje(db: Session) -> list[dict]:
    documentos = DocumentsTypesTravelsRepository.listar_tipos_documentos_viaje(db)
    return [{"id": d.document_type_id, "name": d.document_category} for d in documentos]
