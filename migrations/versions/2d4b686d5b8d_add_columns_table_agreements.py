"""add columns table agreements

Revision ID: 2d4b686d5b8d
Revises: 012cff2d0a41
Create Date: 2026-10-09 15:45:40.995240

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d4b686d5b8d'
down_revision: Union[str, Sequence[str], None] = '012cff2d0a41'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("agreements", sa.Column("precedents", sa.Text(), nullable=True))
    op.add_column("agreements", sa.Column("justification", sa.Text(), nullable=True))
    op.add_column("agreements", sa.Column("scope", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("agreements", "scope")
    op.drop_column("agreements", "justification")
    op.drop_column("agreements", "precedents")