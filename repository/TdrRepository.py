import json

from sqlalchemy import text
from sqlalchemy.orm import Session

from dto.TermsReferenceDTO import TermsReferenceCreate


def guardar_tdr(
    user_id: int,
    tdr: TermsReferenceCreate,
    db: Session
):
    query = """
        SELECT public.insert_terms_reference(
            :program_id,
            :description,
            :approval_flow_id,
            :created_by_user_id,
            CAST(:tdr_form AS jsonb)
        )
    """

    result = db.execute(
        text(query),
        {
            "program_id": tdr.program_id,
            "description": tdr.description,
            "approval_flow_id": tdr.approval_flow_id,
            "created_by_user_id": user_id,
            "tdr_form": json.dumps([
                field.model_dump()
                for field in tdr.tdr_form
            ])
        }
    )

    return result.scalar_one()


def obtener_campos_tdr(
    approval_flow_id: int,
    db: Session
):
    query = """
        SELECT public.form_tdr(:approval_flow_id)
    """

    result = db.execute(
        text(query),
        {
            "approval_flow_id": approval_flow_id
        }
    )

    return result.scalar_one()