"""Campos para el historial del label dinamico en procesos de aprobación

Revision ID: f45e06efc8a6
Revises: dd69f8b8df89
Create Date: 2026-09-14 10:50:16.013473

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f45e06efc8a6'
down_revision: Union[str, Sequence[str], None] = 'dd69f8b8df89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        ALTER TABLE IF EXISTS approval_request_history
            ADD COLUMN state_label text;


    """)
    # ### end Alembic commands ###
def downgrade():
    op.execute("""
        ALTER TABLE IF EXISTS approval_request_history
            DROP COLUMN IF EXISTS state_label;
    """)
