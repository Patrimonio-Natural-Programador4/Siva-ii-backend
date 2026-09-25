"""chore(migrations): merge heads

Revision ID: e8cf13c49eee
Revises: 22bfa8b11ad1, ba03ea7600b5
Create Date: 2026-09-16 14:00:43.374090

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8cf13c49eee'
down_revision: Union[str, Sequence[str], None] = ('22bfa8b11ad1', 'ba03ea7600b5')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
