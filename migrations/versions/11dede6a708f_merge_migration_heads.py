"""merge migration heads

Revision ID: 11dede6a708f
Revises: 78fed72feb10, 988e3eb84193
Create Date: 2026-10-23 15:08:05.049615

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11dede6a708f'
down_revision: Union[str, Sequence[str], None] = ('78fed72feb10', '988e3eb84193')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
