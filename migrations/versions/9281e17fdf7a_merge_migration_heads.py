"""Merge migration heads

Revision ID: 9281e17fdf7a
Revises: 3520dca895ed, 27d92f44f2fc
Create Date: 2026-09-25 11:25:16.730909

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9281e17fdf7a'
down_revision: Union[str, Sequence[str], None] = ('3520dca895ed', '27d92f44f2fc')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
