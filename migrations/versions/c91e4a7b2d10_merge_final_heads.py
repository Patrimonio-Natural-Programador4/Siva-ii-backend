"""Merge final migration heads

Revision ID: c91e4a7b2d10
Revises: 2a82f539572a, 304fa88ea04e
Create Date: 2026-09-11
"""

from typing import Sequence, Union

from alembic import op


revision: str = 'c91e4a7b2d10'
down_revision: Union[str, Sequence[str], None] = (
    '2a82f539572a',
    '304fa88ea04e',
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass