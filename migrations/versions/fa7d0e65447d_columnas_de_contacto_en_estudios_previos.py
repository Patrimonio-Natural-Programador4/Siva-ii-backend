"""Columnas de contacto en estudios previos

Revision ID: fa7d0e65447d
Revises: 81413e9b30d0
Create Date: 2026-11-17 08:12:32.055861

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa7d0e65447d'
down_revision: Union[str, Sequence[str], None] = '81413e9b30d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE IF EXISTS previous_studies
            ADD COLUMN contact_ei integer;

        ALTER TABLE IF EXISTS previous_studies
            ADD COLUMN participants_ei integer;

    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE IF EXISTS previous_studies
            DROP COLUMN IF EXISTS contact_ei;

        ALTER TABLE IF EXISTS previous_studies
            DROP COLUMN IF EXISTS participants_ei;
    """)
