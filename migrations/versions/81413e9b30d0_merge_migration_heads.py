"""merge migration heads

Revision ID: 81413e9b30d0
Revises: 6bd280f0fa76, 8c17a0241c8c
Create Date: 2026-11-09 19:37:26.273061

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '81413e9b30d0'
down_revision: Union[str, Sequence[str], None] = ('6bd280f0fa76', '8c17a0241c8c')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
