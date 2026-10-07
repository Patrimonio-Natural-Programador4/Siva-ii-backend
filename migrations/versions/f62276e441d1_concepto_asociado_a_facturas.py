"""Concepto asociado a facturas

Revision ID: f62276e441d1
Revises: 6dc769f1784f
Create Date: 2026-10-06 21:19:03.513711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f62276e441d1'
down_revision: Union[str, Sequence[str], None] = '6dc769f1784f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE IF EXISTS travel_legalizations
            ADD COLUMN concept_id integer;

        ALTER TABLE IF EXISTS travel_legalizations
            ADD CONSTRAINT travel_legalizations_concepts_fkey FOREIGN KEY (concept_id)
            REFERENCES expense_advance_concepts (expense_advance_concept_id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            NOT VALID;
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE IF EXISTS travel_legalizations DROP CONSTRAINT IF EXISTS travel_legalizations_concepts_fkey;

        ALTER TABLE IF EXISTS travel_legalizations
            DROP COLUMN IF EXISTS concept_id;
    """)
