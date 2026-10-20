"""merge migration heads

Revision ID: 988e3eb84193
Revises: 2d4b686d5b8d, 952c9db0582f
Create Date: 2026-10-19 09:39:59.413407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '988e3eb84193'
down_revision: Union[str, Sequence[str], None] = ('2d4b686d5b8d', '952c9db0582f')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
