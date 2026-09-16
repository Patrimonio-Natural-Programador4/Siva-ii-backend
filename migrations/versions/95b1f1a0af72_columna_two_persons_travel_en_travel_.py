"""columna_two_persons_travel_en_travel_requests

Revision ID: 95b1f1a0af72
Revises: f67e554cd5d4
Create Date: 2026-08-26 14:20:10.588963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95b1f1a0af72'
down_revision: Union[str, Sequence[str], None] = 'f67e554cd5d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE IF EXISTS public.travel_requests
            ADD COLUMN IF NOT EXISTS two_persons_travel boolean DEFAULT false;
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE IF EXISTS public.travel_requests
            DROP COLUMN IF EXISTS two_persons_travel;
    """)

