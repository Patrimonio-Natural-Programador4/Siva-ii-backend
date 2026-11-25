import logging
from sqlalchemy import text
from sqlalchemy.orm import Session
from dto.Document_types_ECDTO import Document_types_EC
from exceptions import PruebaNotFoundError


def list_document_types_ec(db: Session) -> Document_types_EC:
    try:
        query = text("""
            SELECT json_build_object(
                'documentos', (
                    SELECT COALESCE(json_agg(t), '[]'::json)
                    FROM (
                        SELECT dta.id,
                               dta.is_required,
                               dta.description
                        FROM documents_types_agreements dta
                    ) t
                ),
                'documentos_evaluacion', (
                    SELECT COALESCE(json_agg(t), '[]'::json)
                    FROM (
                        SELECT aa.capacity_assessments_id,
                               dta.id AS document_type_id,
                               dta.description
                        FROM attachment_agreement aa
                        INNER JOIN capacity_assessments ca
                                ON aa.capacity_assessments_id = ca.id
                        INNER JOIN documents_types_agreements dta
                                ON aa.documents_types_agreements_id = dta.id
                    ) t
                ),
                'id', (SELECT id FROM attachment_agreement aa LIMIT 1)
            )::text AS resultado
        """)

        row = db.execute(query).fetchone()
        return Document_types_EC(resultado=row.resultado if row else None)
    except Exception as e:
        logging.error(f"Failed to list Document_types_EC: {str(e)}")
        raise PruebaNotFoundError(str(e))
