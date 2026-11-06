"""add_column_is_deleted_table_EC_05_11_2026

Revision ID: 7dcdd838aa64
Revises: a07abe797b62
Create Date: 2026-11-05 14:55:22.958699

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7dcdd838aa64'
down_revision: Union[str, Sequence[str], None] = 'a07abe797b62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
           "capacity_assessments",
           sa.Column("is_deleted", sa.Boolean(), nullable=True ),
       )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("capacity_assessments", "is_deleted")

