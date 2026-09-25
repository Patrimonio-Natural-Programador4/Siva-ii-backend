"""chore(migrations): merge heads

Revision ID: 22bfa8b11ad1
Revises: 25adff2dcef2, 688bd1f97b40
Create Date: 2026-09-16 11:33:20.398064

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22bfa8b11ad1'
down_revision: Union[str, Sequence[str], None] = ('25adff2dcef2', '688bd1f97b40')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
