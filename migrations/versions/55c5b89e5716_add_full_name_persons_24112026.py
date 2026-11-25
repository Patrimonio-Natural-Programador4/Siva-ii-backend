"""add full_name persons 24112026

Revision ID: 55c5b89e5716
Revises: c8e14ab6d932
Create Date: 2026-11-24 14:18:01.619601

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "55c5b89e5716"
down_revision: Union[str, Sequence[str], None] = "c8e14ab6d932"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE persons ADD COLUMN full_name text
        GENERATED ALWAYS AS (
            initcap(btrim(
                COALESCE(first_name, ''::citext)::text || ' ' ||
                COALESCE(other_name, ''::citext)::text || ' ' ||
                COALESCE(last_name, ''::citext)::text || ' ' ||
                COALESCE(other_last_name, ''::citext)::text
            ))
        ) STORED NULL
    """)


def downgrade() -> None:
    op.drop_column("persons", "full_name")
