"""Columnas días y tiempos flujos de aprobación

Revision ID: 6dc769f1784f
Revises: 402de707bf59
Create Date: 2026-10-06 09:56:10.969186

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6dc769f1784f'
down_revision: Union[str, Sequence[str], None] = '402de707bf59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE IF EXISTS approval_flow_steps
            ADD COLUMN days_for_approval integer;

        ALTER TABLE IF EXISTS programs
            ADD COLUMN first_alert_approval integer;

        ALTER TABLE IF EXISTS programs
            ADD COLUMN secod_alert_approval integer;
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE IF EXISTS approval_flow_steps
            DROP COLUMN IF EXISTS days_for_approval;

        ALTER TABLE IF EXISTS programs
            DROP COLUMN IF EXISTS first_alert_approval;

        ALTER TABLE IF EXISTS programs
            DROP COLUMN IF EXISTS secod_alert_approval;
    """)
