"""Add invited traveler document

Revision ID: 111c46337581
Revises: 817834776361
Create Date: 2026-09-23 12:52:27.165634

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '111c46337581'
down_revision: Union[str, Sequence[str], None] = '817834776361'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('travel_requests', sa.Column('invited_traveler_document', sa.Text(), nullable=True))
    op.add_column('travel_requests', sa.Column('invited_traveler_document_type_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'travel_requests_invited_traveler_document_type_id_fkey',
        'travel_requests', 'document_types',
        ['invited_traveler_document_type_id'], ['id']
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('travel_requests_invited_traveler_document_type_id_fkey', 'travel_requests', type_='foreignkey')
    op.drop_column('travel_requests', 'invited_traveler_document_type_id')
    op.drop_column('travel_requests', 'invited_traveler_document')
