"""add agreement_type and modality

Revision ID: fd5ec84b6db5
Revises: 1b36b367e930
Create Date: 2026-10-19 09:46:56.013068

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd5ec84b6db5'
down_revision: Union[str, Sequence[str], None] = '1b36b367e930'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "previous_studies",
        sa.Column("agreement_type_id", sa.Integer(), nullable=True),
    )
    op.add_column(
        "previous_studies",
        sa.Column("modality_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        "fk_previous_studies_agreement_type_id",
        "previous_studies",
        "agreement_types",
        ["agreement_type_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_previous_studies_modality_id",
        "previous_studies",
        "modalities",
        ["modality_id"],
        ["id"],
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_previous_studies_modality_id", "previous_studies", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_previous_studies_agreement_type_id", "previous_studies", type_="foreignkey"
    )
    op.drop_column("previous_studies", "modality_id")
    op.drop_column("previous_studies", "agreement_type_id")
