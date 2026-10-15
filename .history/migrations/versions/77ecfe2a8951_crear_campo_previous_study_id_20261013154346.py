"""crear tabla usuarios

Revision ID: 77ecfe2a8951
Revises: 543a08cb0cce
Create Date: 2026-10-13 15:37:34.953860

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77ecfe2a8951'
down_revision: Union[str, Sequence[str], None] = '543a08cb0cce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    op.add_column(
        'agreements',
        sa.Column('prevous_study_id', sa.BigInteger, sa.ForeignKey('previous_studies.id'), nullable=True)
    )


def downgrade() -> None:
    "
