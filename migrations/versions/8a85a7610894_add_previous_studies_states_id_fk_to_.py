"""add previous_studies_states_id fk to previous_studies

Revision ID: 8a85a7610894
Revises: 629906209487
Create Date: 2026-09-02 11:34:47.193939

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a85a7610894'
down_revision: Union[str, Sequence[str], None] = '629906209487'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "previous_studies",
        sa.Column("previous_studies_states_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        "fk_previous_studies_previous_studies_states",
        "previous_studies",
        "previous_studies_states",
        ["previous_studies_states_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_previous_studies_previous_studies_states",
        "previous_studies",
        type_="foreignkey",
    )
    op.drop_column("previous_studies", "previous_studies_states_id")