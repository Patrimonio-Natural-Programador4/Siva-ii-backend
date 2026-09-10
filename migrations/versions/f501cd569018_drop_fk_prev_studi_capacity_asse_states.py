"""drop fk prev_studi_capacity_asse_states

Revision ID: f501cd569018
Revises: 028b227fa2db
Create Date: 2026-09-02 11:02:46.194586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f501cd569018'
down_revision: Union[str, Sequence[str], None] = '028b227fa2db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "fk_previous_studies_capacity_assessments_states",
        "previous_studies",
        type_="foreignkey",
    )
    op.drop_column("previous_studies", "capacity_assessments_states_id")


def downgrade() -> None:
    op.add_column(
        "previous_studies",
        sa.Column("capacity_assessments_states_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        "fk_previous_studies_capacity_assessments_states",
        "previous_studies",
        "capacity_assessments_states",
        ["capacity_assessments_states_id"],
        ["id"],
    )