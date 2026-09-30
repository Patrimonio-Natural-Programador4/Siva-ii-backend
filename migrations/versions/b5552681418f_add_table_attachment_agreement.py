"""add_table_attachment_agreement

Revision ID: b5552681418f
Revises: f00b0991d689
Create Date: 2026-09-29 09:22:29.492470

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5552681418f'
down_revision: Union[str, Sequence[str], None] = 'f00b0991d689'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
          "attachment_agreement",
          sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
          sa.Column("attachment_name", sa.Text(), nullable=False),
          sa.Column("path_document", sa.Text(), nullable=False),
          sa.Column("capacity_assessments_id", sa.Integer(), nullable=False),
          sa.Column("observations", sa.Text(), nullable=False),
          sa.Column("documents_types_agreements_id", sa.Integer(), nullable=False),
          sa.ForeignKeyConstraint(['capacity_assessments_id'], ['capacity_assessments.id'], name='fk_attachment_agreements_capacity_assessments'),
          sa.ForeignKeyConstraint(['documents_types_agreements_id'], ['documents_types_agreements.id'], name='fk_attachment_agreements_documents_types_agreements'),
          
          
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('attachment_agreement')
