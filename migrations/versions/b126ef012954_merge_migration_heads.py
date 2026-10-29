"""merge migration heads

Revision ID: b126ef012954
Revises: 59f926205aaf, c2a5d998e230
Create Date: 2026-10-29 06:02:18.875609

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b126ef012954'
down_revision: Union[str, Sequence[str], None] = ('59f926205aaf', 'c2a5d998e230')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
