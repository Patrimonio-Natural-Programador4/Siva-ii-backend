"""add_column_table_disbursement

Revision ID: f0b4627c22af
Revises: 3e2956da9f00
Create Date: 2026-10-19 15:37:30.645301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0b4627c22af'
down_revision: Union[str, Sequence[str], None] = '3e2956da9f00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.add_column(
        "disbursement",
        sa.Column("agreement_id", sa.BigInteger(), nullable=True),
    )
    
    op.add_column(
            "disbursement",
            sa.Column("previous_studies_id", sa.BigInteger(), nullable=True),
        )
    
    op.create_foreign_key(
            "fk_agreements_products_agreements",
            "disbursement",
            "agreements",
            ["agreement_id"],
            ["id"],
        )
   
    op.create_foreign_key(
        "fk_disbursement_previous_studies",
        "disbursement",
        "previous_studies",
        ["previous_studies_id"],
        ["id"],
    )
   

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_agreements_products_agreements", "disbursement", type_="foreignkey"
    )
    
    op.drop_constraint(
            "fk_disbursement_previous_studies", "disbursement", type_="foreignkey"
        )
   
    op.drop_column("disbursement", "agreement_id")
    op.drop_column("disbursement", "previous_studies_id")
   