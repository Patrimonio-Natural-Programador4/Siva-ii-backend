import logging
from sqlalchemy import text
from sqlalchemy.orm import Session
from entity.documents_approval import DocumentsApproval
from exceptions import PruebaCreationError, PruebaNotFoundError


def listar(db: Session) -> list[DocumentsApproval]:
    try:
        return db.query(DocumentsApproval).order_by(DocumentsApproval.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list DocumentsApproval: {str(e)}")
        raise PruebaNotFoundError(str(e))


def listar_documentos_aprobacion(db: Session):
    result = db.execute(text("""
            SELECT
                da.id,
                da.name AS documento,
                ac.name AS categoria,
                p.name AS programa
            FROM documents_approval da
            INNER JOIN approval_categories ac
                ON ac.category_id = da.approval_category_id
            INNER JOIN programs p
                ON p.id = da.program_id
            ORDER BY da.id
        """))

    return [
        {
            "id": row.id,
            "documento": row.documento,
            "categoria": row.categoria,
            "programa": row.programa
        }
        for row in result
    ]

# obtiene el doc por nombre para evitar duplicados
def obtener_por_nombre(name: str, db: Session) -> DocumentsApproval | None:
    try:
        return db.query(DocumentsApproval).filter(DocumentsApproval.name.ilike(name.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get program by name: {str(e)}")
        raise PruebaNotFoundError(str(e))

# crea el doc
def crear(document_approval: DocumentsApproval, db: Session) -> DocumentsApproval:
    try:
        db.add(document_approval)
        db.commit()
        db.refresh(document_approval)
        return document_approval
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create document_approval: {str(e)}")
        raise PruebaCreationError(str(e))

#obtiene doc por id 

def obtener_por_id(id:int, db:Session)-> DocumentsApproval:
    try:
        print("Buscando ID:", id)

        doc = db.query(DocumentsApproval)\
                .filter(DocumentsApproval.id == id)\
                .first()

        print("Resultado:", doc)

        return doc

    except Exception as e:
        logging.error(f"Failed to find DocumentsApproval by id: {str(e)}")
        return None
       
    
def actualizar(document_approval:DocumentsApproval, db:Session)-> DocumentsApproval:
    try:
        db.commit()
        db.refresh(document_approval)
        return document_approval
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create document_approval: {str(e)}  ")
        raise PruebaCreationError(str(e))
    