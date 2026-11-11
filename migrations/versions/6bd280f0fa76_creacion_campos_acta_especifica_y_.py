"""creacion campos acta especifica y acuerd macro en estudios previos

Revision ID: 6bd280f0fa76
Revises: 3778370df902
Create Date: 2026-11-06 14:26:53.496850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6bd280f0fa76'
down_revision: Union[str, Sequence[str], None] = '3778370df902'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
tablee = "previous_studies"

def upgrade() -> None:
    
    op.add_column(
        tablee,
        sa.Column("is_specifi_minute", sa.Boolean(), nullable=True ),
    )
    
    op.add_column(
        tablee,
        sa.Column("framework_agreement_id", sa.BigInteger(), nullable=True),
    )
    
    op.create_foreign_key(
        "fk_previous_studies_agreements",
        "previous_studies",
        "agreements",
        ["framework_agreement_id"],
        ["id"],
    )
    


def downgrade() -> None:
    op.drop_column("previous_studies", "is_specifi_minute")
    op.drop_column("previous_studies", "framework_agreement_id")
    op.drop_constraint(
        "fk_previous_studies_agreements", tablee, type_="foreignkey"
    )