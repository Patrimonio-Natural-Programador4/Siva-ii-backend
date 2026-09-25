"""Campos de contacto de emergencia en la tabla de travel_requests

Revision ID: f4238ea967cc
Revises: 247ca2e99043
Create Date: 2026-08-21 11:01:24.121094

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4238ea967cc'
down_revision: Union[str, Sequence[str], None] = '247ca2e99043'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        
ALTER TABLE IF EXISTS travel_requests
    ADD COLUMN emergency_contact text;

ALTER TABLE IF EXISTS travel_requests
    ADD COLUMN emergency_phone text;

ALTER TABLE IF EXISTS travel_requests
    ADD COLUMN emergency_relationship text;
    """)


def downgrade() -> None:
    op.execute("""
ALTER TABLE IF EXISTS travel_requests
    DROP COLUMN IF EXISTS emergency_contact;
ALTER TABLE IF EXISTS travel_requests
    DROP COLUMN IF EXISTS emergency_phone;
ALTER TABLE IF EXISTS travel_requests
    DROP COLUMN IF EXISTS emergency_relationship;
    """)