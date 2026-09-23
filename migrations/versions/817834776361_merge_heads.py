"""Merge heads

Revision ID: 817834776361
Revises: 3520dca895ed, 95558a709af0
Create Date: 2026-09-23 12:52:06.400678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '817834776361'
down_revision: Union[str, Sequence[str], None] = ('3520dca895ed', '95558a709af0')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
