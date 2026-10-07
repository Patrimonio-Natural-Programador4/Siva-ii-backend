"""create_vw_travel_general

Revision ID: 87c96fd21f86
Revises: 402de707bf59
Create Date: 2026-10-02 13:07:23.990651

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87c96fd21f86'
down_revision: Union[str, Sequence[str], None] = '402de707bf59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
DROP VIEW IF EXISTS public.vw_travel_general CASCADE;
CREATE OR REPLACE VIEW public.vw_travel_general AS
SELECT DISTINCT
    tr.code AS "code", 
    COALESCE(u.full_name, tr.guest_name) AS "traveler", 
    COALESCE(tr.request_date, CAST(tr.created_at AS date)) AS "request_date",
    tr.travel_start_date AS "travel_start_date",
    tr.travel_end_date AS "travel_end_date",
    tr.requires_advance_payment AS "requires_advance_payment",
    tr.advance_amount AS "requested_advance_amount", 
    tr.total_days AS "total_days", 
    ts.name AS "status",
    rub.rubros AS "budget_item",
    act.description AS "expense_category", 
    tr.activity_purpose AS "travel_purpose",
    tr.additional_comments AS "general_additional_comments", 
    sup.full_name AS "supervisor", 
    prog.name AS "program",
    tr.is_international AS "is_international_travel", 
    CASE WHEN tr.is_guest = true THEN false ELSE true END AS "is_employee_travel",
    tr.is_guest AS "is_guest_travel", 
    tr.traveler_birth_date AS "birth_date", 
    tr.mobile_phone AS "mobile_phone", 
    tr.emergency_contact_name AS "emergency_contact_name", 
    tr.emergency_contact_phone AS "emergency_contact_phone", 
    tr.emergency_relationship AS "emergency_relationship", 
    tr.includes_food AS "includes_food"
FROM public.travel_requests tr
LEFT JOIN public.users u ON tr.traveler_user_id = u.id
LEFT JOIN public.travel_status ts ON tr.travel_status_id = ts.status_id
LEFT JOIN public.rubros rub ON tr.rubro_id = rub.id
LEFT JOIN public.activities act ON tr.activity_id = act.id
LEFT JOIN public.users sup ON u.supervisor_user_id = sup.id
LEFT JOIN public.programs prog ON tr.program_id = prog.id;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP VIEW IF EXISTS public.vw_travel_general;")
