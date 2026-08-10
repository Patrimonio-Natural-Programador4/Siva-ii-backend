"""Implementación flag de usuarios invitados

Revision ID: b31e37378e7a
Revises: 
Create Date: 2026-08-06 10:56:41.455010

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b31e37378e7a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.execute("""
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS is_guest boolean;
    """)

def downgrade():
    op.execute("""
        ALTER TABLE users
        DROP COLUMN IF EXISTS is_guest;
    """)
