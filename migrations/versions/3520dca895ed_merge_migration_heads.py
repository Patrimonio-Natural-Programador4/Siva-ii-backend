"""Merge migration heads

Revision ID: 3520dca895ed
Revises: 25adff2dcef2, ba03ea7600b5
Create Date: 2026-09-17 16:35:47.719230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3520dca895ed'
down_revision: Union[str, Sequence[str], None] = ('25adff2dcef2', 'ba03ea7600b5')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
