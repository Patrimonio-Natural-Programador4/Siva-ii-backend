"""Crear columna delega responsable

Revision ID: a1eac9267353
Revises: 3778370df902
Create Date: 2026-11-06 11:24:43.678430

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1eac9267353'
down_revision: Union[str, Sequence[str], None] = '3778370df902'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    op.execute("""
        ALTER TABLE approval_flow_steps
        ADD COLUMN IF NOT EXISTS enable_delegation boolean;
    """)

def downgrade():
    op.execute("""
        ALTER TABLE approval_flow_steps
        DROP COLUMN IF EXISTS enable_delegation;
    """)

