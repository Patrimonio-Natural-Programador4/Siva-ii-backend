"""Actualizacion flujos aprobacion reglas

Revision ID: 2aeebdfae87f
Revises: d35f13a251e5
Create Date: 2026-11-25 12:27:04.733101

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2aeebdfae87f'
down_revision: Union[str, Sequence[str], None] = 'd35f13a251e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    op.execute("""
        ALTER TABLE approval_flows
        ADD COLUMN IF NOT EXISTS configuration_rules text;
    """)

def downgrade():
    op.execute("""
        ALTER TABLE approval_flows
        DROP COLUMN IF EXISTS configuration_rules;
    """)
