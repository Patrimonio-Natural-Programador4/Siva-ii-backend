"""create_vw_travel_accommodations

Revision ID: 675840cc30fc
Revises: 394847672fd6
Create Date: 2026-10-02 13:07:24.429246

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '675840cc30fc'
down_revision: Union[str, Sequence[str], None] = '394847672fd6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
DROP VIEW IF EXISTS public.vw_travel_accommodations CASCADE;
CREATE OR REPLACE VIEW public.vw_travel_accommodations AS
SELECT DISTINCT
    tr.code AS "code", 
    COALESCE(u.full_name, tr.guest_name) AS "traveler",
    reg_acc_dep.name AS "accommodation_department", 
    reg_acc_mun.name AS "accommodation_municipality",
    ta.check_in_date AS "check_in_date", 
    ta.check_out_date AS "check_out_date", 
    ta.comments AS "accommodation_additional_comments"
FROM public.travel_requests tr
INNER JOIN public.travel_accommodations ta ON tr.travel_request_id = ta.travel_request_id
LEFT JOIN public.users u ON tr.traveler_user_id = u.id
LEFT JOIN public.regions reg_acc_mun ON ta.municipality_id = reg_acc_mun.id
LEFT JOIN public.regions reg_acc_dep ON reg_acc_mun.region_id = reg_acc_dep.id;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP VIEW IF EXISTS public.vw_travel_accommodations;")
