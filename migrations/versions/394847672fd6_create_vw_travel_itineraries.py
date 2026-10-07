"""create_vw_travel_itineraries

Revision ID: 394847672fd6
Revises: 87c96fd21f86
Create Date: 2026-10-02 13:07:24.203198

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '394847672fd6'
down_revision: Union[str, Sequence[str], None] = '87c96fd21f86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
DROP VIEW IF EXISTS public.vw_travel_itineraries CASCADE;
CREATE OR REPLACE VIEW public.vw_travel_itineraries AS
SELECT DISTINCT
    tr.code AS "code", 
    COALESCE(u.full_name, tr.guest_name) AS "traveler",
    reg_orig_dep.name AS "origin_department", 
    reg_orig_mun.name AS "origin_municipality",
    reg_dest_dep.name AS "destination_department", 
    reg_dest_mun.name AS "destination_municipality",
    COALESCE(ti.requires_air_tickets, tr.requires_tickets) AS "requires_air_tickets", 
    ti.travel_date AS "travel_date",
    ti.departure_time AS "estimated_departure_time", 
    ti.is_rural_area AS "is_rural_destination", 
    ti.comments AS "itinerary_additional_comments"
FROM public.travel_requests tr
INNER JOIN public.travel_itineraries ti ON tr.travel_request_id = ti.travel_request_id
LEFT JOIN public.users u ON tr.traveler_user_id = u.id
LEFT JOIN public.regions reg_orig_mun ON ti.origin_municipality_id = reg_orig_mun.id
LEFT JOIN public.regions reg_orig_dep ON reg_orig_mun.region_id = reg_orig_dep.id
LEFT JOIN public.regions reg_dest_mun ON ti.destination_municipality_id = reg_dest_mun.id
LEFT JOIN public.regions reg_dest_dep ON reg_dest_mun.region_id = reg_dest_dep.id;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP VIEW IF EXISTS public.vw_travel_itineraries;")
