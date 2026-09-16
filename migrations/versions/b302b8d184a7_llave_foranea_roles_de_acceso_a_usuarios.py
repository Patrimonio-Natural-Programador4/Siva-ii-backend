"""Llave foranea roles de acceso a usuarios

Revision ID: b302b8d184a7
Revises: 818443d98595
Create Date: 2026-09-11 04:06:31.699592

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b302b8d184a7'
down_revision: Union[str, Sequence[str], None] = '818443d98595'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE IF EXISTS model_has_roles
        ADD FOREIGN KEY (model_id)
        REFERENCES users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID;
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE IF EXISTS model_has_roles
    DROP CONSTRAINT IF EXISTS model_has_roles_model_id_fkey;
    """)


