import logging
from sqlalchemy.orm import Session
from exceptions import PruebaNotFoundError, PruebaCreationError
from entity.attachment_agreement import Attachment_Agreement

logger = logging.getLogger(__name__)


def save_attachment_agreement( 
     capacity_assessments_id: int,  # eval capa
     attachment_name: str, # nombre archivo
     path_document: str, #ruta archivo
     db: Session,
     documents_types_agreements_id: int | None = None, # tipo docs acuerdos
     observations: str | None = None
    ) -> Attachment_Agreement:
        try:
            nuevo_registro = Attachment_Agreement(
                attachment_name=attachment_name, # nombre archivo
                path_document=str(path_document),  #ruta archivo
                capacity_assessments_id=capacity_assessments_id, # eval capa
                documents_types_agreements_id=documents_types_agreements_id, # tipo docs acuerdos
                observations=observations
            )
            db.add(nuevo_registro)
            db.commit()
            db.refresh(nuevo_registro)
            
            return nuevo_registro
        except Exception as e:
            db.rollback()
            logger.error(f"Error al guardar archivos acuerdos en BD evaluación de capacidades {capacity_assessments_id}: {str(e)}")
            raise PruebaCreationError(str(e))
                              
                             


def save_or_replace_attachment_agreement(
    capacity_assessments_id: int,
    attachment_name: str,
    path_document: str,
    db: Session,
    documents_types_agreements_id: int | None = None,
    observations: str | None = None
) -> Attachment_Agreement:
    return save_attachment_agreement(capacity_assessments_id, attachment_name, path_document, db, documents_types_agreements_id, observations)


def get_attachment_agreement_by_capacity_assessments_id(
    capacity_assessments_id: int,
    db: Session
) -> Attachment_Agreement | None:
    try:
        return (
            db.query(Attachment_Agreement)
            .filter(Attachment_Agreement.capacity_assessments_id == capacity_assessments_id)
            .order_by(Attachment_Agreement.id.desc())
            .first()
        )
    except Exception as e:
        logger.error(f"Error al obtener archivo  para evaluación de capacidad {capacity_assessments_id}: {str(e)}")
        raise PruebaNotFoundError(str(e))


def list_attachment_agreement_by_capacity_assessments_id(
    capacity_assessments_id: int,
    db: Session
) -> list[Attachment_Agreement]:
    try:
        
        print(capacity_assessments_id)
        return (
            db.query(Attachment_Agreement)
            .filter(Attachment_Agreement.capacity_assessments_id == capacity_assessments_id)
            .order_by(Attachment_Agreement.id.asc())
            .all()
        )
    except Exception as e:
        logger.error(f"Error al listar archivos evaluación de capacidad {capacity_assessments_id}: {str(e)}")
        raise PruebaNotFoundError(str(e))
