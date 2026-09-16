"""create table previous_studies_states

Revision ID: 629906209487
Revises: f501cd569018
Create Date: 2026-09-02 11:28:24.398366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '629906209487'
down_revision: Union[str, Sequence[str], None] = 'f501cd569018'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "previous_studies_states",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("state", sa.Text(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("previous_studies_states")