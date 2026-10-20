"""merge heads disbursement y previous_study

Revision ID: b27f29f35ae0
Revises: f0b4627c22af, 988e3eb84193
Create Date: 2026-10-20 18:06:31.024823

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b27f29f35ae0'
down_revision: Union[str, Sequence[str], None] = ('f0b4627c22af', '988e3eb84193')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
