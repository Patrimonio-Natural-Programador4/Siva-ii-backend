"""Asignación rubros y actividades a viajes

Revision ID: bda72b876987
Revises: a7b54d2875b9
Create Date: 2026-08-06 14:56:59.722542

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bda72b876987'
down_revision: Union[str, Sequence[str], None] = 'a7b54d2875b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        ALTER TABLE IF EXISTS public.travel_requests
                ADD COLUMN rubro_id integer;

            ALTER TABLE IF EXISTS public.travel_requests
                ADD COLUMN short_rubro text;

            ALTER TABLE IF EXISTS public.travel_requests
                ADD COLUMN year_rubro integer;

            ALTER TABLE IF EXISTS public.travel_requests
                ADD COLUMN activity_id integer;
            ALTER TABLE IF EXISTS public.travel_requests
                ADD CONSTRAINT travel_requests_rubros_fkey FOREIGN KEY (rubro_id)
                REFERENCES public.rubros (id) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                NOT VALID;

            ALTER TABLE IF EXISTS public.travel_requests
                ADD CONSTRAINT travel_requests_activities_fkey FOREIGN KEY (activity_id)
                REFERENCES public.activities (id) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                NOT VALID;
    """)

def downgrade():
    op.execute("""
        ALTER TABLE IF EXISTS public.travel_requests
            DROP COLUMN IF EXISTS rubro_id;

        ALTER TABLE IF EXISTS public.travel_requests
            DROP COLUMN IF EXISTS short_rubro;

        ALTER TABLE IF EXISTS public.travel_requests
            DROP COLUMN IF EXISTS year_rubro;

        ALTER TABLE IF EXISTS public.travel_requests
            DROP COLUMN IF EXISTS activity_id;

        ALTER TABLE IF EXISTS public.travel_requests
            DROP CONSTRAINT IF EXISTS travel_requests_rubros_fkey;

        ALTER TABLE IF EXISTS public.travel_requests
            DROP CONSTRAINT IF EXISTS travel_requests_activities_fkey;
    """)
