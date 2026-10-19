"""add_column_table_agreements_products

Revision ID: 3e2956da9f00
Revises: 7f75d236ca2d
Create Date: 2026-10-19 15:12:09.606405

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e2956da9f00'
down_revision: Union[str, Sequence[str], None] = '7f75d236ca2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "agreements_products",
        sa.Column("previous_studies_id", sa.BigInteger(), nullable=True),
    )
   
    op.create_foreign_key(
        "fk_agreements_products_previous_studies",
        "agreements_products",
        "previous_studies",
        ["previous_studies_id"],
        ["id"],
    )
   

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_agreements_products_previous_studies", "agreements_products", type_="foreignkey"
    )
   
    op.drop_column("agreements_products", "previous_studies_id")
   