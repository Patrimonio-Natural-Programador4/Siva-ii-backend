"""merge heads

Revision ID: 051f5a1b6c02
Revises: b5552681418f, d8bf70716e4a
Create Date: 2026-09-30 10:11:04.747765

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '051f5a1b6c02'
down_revision: Union[str, Sequence[str], None] = ('b5552681418f', 'd8bf70716e4a')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
