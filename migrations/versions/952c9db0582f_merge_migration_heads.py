"""merge migration heads

Revision ID: 952c9db0582f
Revises: 2b5bdef20470, 6c45250507c2
Create Date: 2026-10-15 13:54:19.474655

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '952c9db0582f'
down_revision: Union[str, Sequence[str], None] = ('2b5bdef20470', '6c45250507c2')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
