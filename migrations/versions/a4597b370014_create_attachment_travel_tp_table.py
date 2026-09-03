"""create_attachment_travel_tp_table

Revision ID: a4597b370014
Revises: 95b1f1a0af72
Create Date: 2026-08-27 12:54:22.124797

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4597b370014'
down_revision: Union[str, Sequence[str], None] = '95b1f1a0af72'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS public.attachment_travel_tp (
            id SERIAL PRIMARY KEY,
            attachment_name TEXT,
            path_document TEXT,
            travel_request_id INTEGER,
            CONSTRAINT fk_attachment_travel_tp_travel_request FOREIGN KEY (travel_request_id)
                REFERENCES public.travel_requests (travel_request_id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        );
    """)


def downgrade() -> None:
    op.execute("""
        DROP TABLE IF EXISTS public.attachment_travel_tp;
    """)
