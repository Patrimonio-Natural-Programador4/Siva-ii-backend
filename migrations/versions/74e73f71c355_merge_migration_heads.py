"""merge migration heads

Revision ID: 74e73f71c355
Revises: 678ff774d697, 051f5a1b6c02
Create Date: 2026-10-02 11:52:15.448972

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74e73f71c355'
down_revision: Union[str, Sequence[str], None] = ('678ff774d697', '051f5a1b6c02')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
