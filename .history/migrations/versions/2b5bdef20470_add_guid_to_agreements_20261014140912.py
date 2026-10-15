"""add guid to agreements

Revision ID: 2b5bdef20470
Revises: 77ecfe2a8951
Create Date: 2026-10-14 14:08:18.251308

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b5bdef20470'
down_revision: Union[str, Sequence[str], None] = '77ecfe2a8951'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'agreements',
        sa.Column(
            'guid',
            postgresql.UUID(as_uuid=True),
            server_default=sa.text('gen_random_uuid()'),
            nullable=False,
        )
        


def downgrade() -> None:
    """Downgrade schema."""
    pass
