"""Crear columna de sesión para productos

Revision ID: 59f926205aaf
Revises: 11dede6a708f
Create Date: 2026-10-27 08:13:40.674767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '59f926205aaf'
down_revision: Union[str, Sequence[str], None] = '11dede6a708f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.execute("""
        ALTER TABLE IF EXISTS agreements_products
    ADD COLUMN session text;
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE IF EXISTS agreements_products
            DROP COLUMN IF EXISTS session;
    """)

