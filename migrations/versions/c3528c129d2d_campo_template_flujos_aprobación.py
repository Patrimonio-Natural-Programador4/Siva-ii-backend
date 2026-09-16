"""Campo template flujos aprobación

Revision ID: c3528c129d2d
Revises: c91e4a7b2d10
Create Date: 2026-09-14 04:46:12.838533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3528c129d2d'
down_revision: Union[str, Sequence[str], None] = 'c91e4a7b2d10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        ALTER TABLE IF EXISTS approval_flows
    ADD COLUMN template text;

    ALTER TABLE IF EXISTS approval_flows
        ADD COLUMN is_parallel_approval boolean;
    """)

def downgrade():
    op.execute("""
        ALTER TABLE IF EXISTS approval_flows
            DROP COLUMN IF EXISTS template;
        ALTER TABLE IF EXISTS approval_flows
            DROP COLUMN IF EXISTS is_parallel_approval;
    """)
