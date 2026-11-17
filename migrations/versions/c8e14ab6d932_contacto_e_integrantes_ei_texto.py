"""Convertir contacto e integrantes EI a texto.

Revision ID: c8e14ab6d932
Revises: fa7d0e65447d
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c8e14ab6d932"
down_revision: Union[str, Sequence[str], None] = "fa7d0e65447d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    for column in ("contact_ei", "participants_ei"):
        op.alter_column(
            "previous_studies", column,
            existing_type=sa.Integer(), type_=sa.Text(),
            existing_nullable=True, postgresql_using=f"{column}::text",
        )


def downgrade() -> None:
    for column in ("contact_ei", "participants_ei"):
        op.alter_column(
            "previous_studies", column,
            existing_type=sa.Text(), type_=sa.Integer(),
            existing_nullable=True, postgresql_using=f"{column}::integer",
        )
