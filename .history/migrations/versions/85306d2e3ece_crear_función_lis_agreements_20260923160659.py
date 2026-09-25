"""Crear función List agreements

Revision ID: 85306d2e3ece
Revises: 028b227fa2db
Create Date: 2026-09-23 15:51:04.790694

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85306d2e3ece'
down_revision: Union[str, Sequence[str], None] = '028b227fa2db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    
    
def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
    DROP FUNCTION IF EXISTS public.list_agreements(
        integer, integer[], integer[], integer[], integer[], 
        integer[], text[], integer[], text[], text[], text, integer, integer
    );
""")