"""insertar estado estudio previo creado

Revision ID: a07abe797b62
Revises: 5c5d9b7a556d
Create Date: 2026-11-04 12:01:05.570745

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a07abe797b62'
down_revision: Union[str, Sequence[str], None] = '5c5d9b7a556d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

#
capacity_assessments_states = sa.table(
    "capacity_assessments_states",
    sa.column("id", sa.Integer),
    sa.column("state", sa.String),
)


def upgrade() -> None:
    """
    op.bulk_insert(
        capacity_assessments_states,
        [
            {"id": 10, "state": "Estudio previo creado"},
        ],
    )"""
    op.execute(
        "INSERT INTO capacity_assessments_states (id, state) "
        "VALUES (10, 'Estudio previo creado')"
    )


def downgrade() -> None:
    op.execute("DELETE FROM capacity_assessments_states WHERE id = 10")
