"""Merge migration heads

Revision ID: 6d6678b4db34
Revises: 028b227fa2db, 660b746b3805
Create Date: 2026-09-11 03:34:25.766000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d6678b4db34'
down_revision: Union[str, Sequence[str], None] = ('028b227fa2db', '660b746b3805')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
