"""create_vw_travel_legalizations

Revision ID: 1045a9d3b2d0
Revises: 675840cc30fc
Create Date: 2026-10-02 13:07:24.661367

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1045a9d3b2d0'
down_revision: Union[str, Sequence[str], None] = '675840cc30fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
DROP VIEW IF EXISTS public.vw_travel_legalizations CASCADE;
CREATE OR REPLACE VIEW public.vw_travel_legalizations AS
SELECT DISTINCT
    tr.code AS "code", 
    COALESCE(u.full_name, tr.guest_name) AS "traveler",
    tl.check_date AS "legalization_date",
    tl.check_number AS "transaction_number",
    tl.beneficiary AS "legalization_beneficiary",
    tl.nit_beneficiary AS "beneficiary_nit",
    rt.name AS "regimen_type",
    tl.subtotal AS "legalized_subtotal",
    tl.iva AS "legalized_iva",
    tl.retention_porcentage AS "retention_percentage",
    tl.retention AS "retention",
    tl.amount_paid AS "total_paid",
    tl.observations_outlay AS "outlay_observations",
    tl.observations AS "legalization_observations"
FROM public.travel_requests tr
INNER JOIN public.travel_legalizations tl ON tr.travel_request_id = tl.travel_request_id
LEFT JOIN public.users u ON tr.traveler_user_id = u.id
LEFT JOIN public.regimen_types rt ON tl.regimen_type_id = rt.id;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP VIEW IF EXISTS public.vw_travel_legalizations;")
