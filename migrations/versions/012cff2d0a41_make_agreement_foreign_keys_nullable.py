"""make agreement foreign keys nullable

Revision ID: 012cff2d0a41
Revises: 543a08cb0cce
Create Date: 2026-10-09 15:41:57.040867

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '012cff2d0a41'
down_revision: Union[str, Sequence[str], None] = '543a08cb0cce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



COLUMNS = [
    "program_id",
    "agreement_type_id",
    "agreement_stage_id",
    "agreement_origin_id",
]


def upgrade() -> None:
    for column in COLUMNS:
        op.alter_column(
            "agreements",
            column,
            existing_type=sa.BigInteger(),
            nullable=True,
        )


def downgrade() -> None:
    for column in COLUMNS:
        op.alter_column(
            "agreements",
            column,
            existing_type=sa.BigInteger(),
            nullable=False,
        )
