"""merge migration heads

Revision ID: d8bf70716e4a
Revises: 111c46337581, 3500f820a5bc
Create Date: 2026-09-29 14:24:26.152481

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8bf70716e4a'
down_revision: Union[str, Sequence[str], None] = ('111c46337581', '3500f820a5bc')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
