"""merge migration heads

Revision ID: 543a08cb0cce
Revises: 1045a9d3b2d0, 8d8c36e5f48e
Create Date: 2026-10-07 10:50:20.269921

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '543a08cb0cce'
down_revision: Union[str, Sequence[str], None] = ('1045a9d3b2d0', '8d8c36e5f48e')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
