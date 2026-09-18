"""Campos para label dinamico de aprobación

Revision ID: dd69f8b8df89
Revises: c3528c129d2d
Create Date: 2026-09-14 04:58:17.555825

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd69f8b8df89'
down_revision: Union[str, Sequence[str], None] = 'c3528c129d2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        ALTER TABLE IF EXISTS approval_flow_steps
            ADD COLUMN approved_label text;

        ALTER TABLE IF EXISTS approval_flow_steps
            ADD COLUMN adjustment_label text;

        ALTER TABLE IF EXISTS approval_flow_steps
            ADD COLUMN assign_reviewer boolean;

        
        ALTER TABLE IF EXISTS approval_flow_steps
            ADD COLUMN pending_label text;

    """)

def downgrade():
    op.execute("""
        ALTER TABLE IF EXISTS approval_flow_steps
            DROP COLUMN IF EXISTS approved_label;
        ALTER TABLE IF EXISTS approval_flow_steps
            DROP COLUMN IF EXISTS adjustment_label;
        ALTER TABLE IF EXISTS approval_flow_steps
            DROP COLUMN IF EXISTS assign_reviewer;
        ALTER TABLE IF EXISTS approval_flow_steps
            DROP COLUMN IF EXISTS pending_label;
    """)
