"""add pillar_id to capacity_assessments

Revision ID: d31437a3cb1a
Revises: fd5ec84b6db5
Create Date: 2026-10-20 22:12:14.235195

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd31437a3cb1a'
down_revision: Union[str, Sequence[str], None] = 'fd5ec84b6db5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "capacity_assessments",
        sa.Column("pillar_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
            "fk_capacity_assessments_pillar_id",
            "capacity_assessments",
            "pillars",
            ["pillar_id"],
            ["id"],
    )

def downgrade() -> None:
    op.drop_constraint(
        "fk_capacity_assessments_pillar_id",
        "capacity_assessments",
        type_="foreignkey",
    )

    op.drop_column(
        "capacity_assessments",
        "pillar_id",
    )
