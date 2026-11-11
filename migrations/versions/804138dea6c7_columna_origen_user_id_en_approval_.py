"""Columna origen_user_id en approval_request_history

Revision ID: 804138dea6c7
Revises: 470b755d506d
Create Date: 2026-11-06 11:58:29.805623

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '804138dea6c7'
down_revision: Union[str, Sequence[str], None] = '470b755d506d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        ALTER TABLE IF EXISTS approval_request_history
            ADD COLUMN origin_user_id integer;
        ALTER TABLE IF EXISTS approval_request_history
            ADD COLUMN origin_approval_rol_id integer;
    """)

def downgrade():
    op.execute("""
        ALTER TABLE IF EXISTS approval_request_history
            DROP COLUMN IF EXISTS origin_user_id;
        ALTER TABLE IF EXISTS approval_request_history
            DROP COLUMN IF EXISTS origin_approval_rol_id;
    """)
