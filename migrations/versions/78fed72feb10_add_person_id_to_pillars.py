"""add person_id to pillars

Revision ID: 78fed72feb10
Revises: d31437a3cb1a
Create Date: 2026-10-21 00:29:15.226561

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78fed72feb10'
down_revision: Union[str, Sequence[str], None] = 'd31437a3cb1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "pillars",
        sa.Column("person_id", sa.Integer(), nullable=True),
    )

    op.create_foreign_key(
        "fk_pillars_person_id",
        "pillars",
        "persons",
        ["person_id"],
        ["id"],
    )

def downgrade() -> None:
    op.drop_constraint(
        "fk_pillars_person_id", "pillars", type_="foreignkey"
    )
    op.drop_column("pillars", "person_id")
