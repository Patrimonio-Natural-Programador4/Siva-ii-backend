"""Implementación flag de activities asociado a gastos logisticos

Revision ID: a7b54d2875b9
Revises: b31e37378e7a
Create Date: 2026-08-06 11:35:08.490300

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7b54d2875b9'
down_revision: Union[str, Sequence[str], None] = 'b31e37378e7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        ALTER TABLE activities
        ADD COLUMN IF NOT EXISTS is_logistics_expense_associate boolean;
    """)

def downgrade():
    op.execute("""
        ALTER TABLE activities
        DROP COLUMN IF EXISTS is_logistics_expense_associate;
    """)

