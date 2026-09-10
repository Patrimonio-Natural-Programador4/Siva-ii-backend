"""crear_tabla_delegacion_usuarios_viajes

Revision ID: d4b8e21a9c37
Revises: 660b746b3805, 028b227fa2db
Create Date: 2026-09-09 14:55:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'd4b8e21a9c37'
down_revision: Union[str, Sequence[str], None] = ('660b746b3805', '028b227fa2db')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users_delegate',
        sa.Column('delegation_id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('responsable_id', sa.BigInteger(), nullable=False),
        sa.Column('delegate_id', sa.BigInteger(), nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(precision=6), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['responsable_id'], ['users.id'], name='fk_users_delegate_responsable'),
        sa.ForeignKeyConstraint(['delegate_id'], ['users.id'], name='fk_users_delegate_delegate'),
        sa.PrimaryKeyConstraint('delegation_id', name='users_delegate_pkey'),
        info={'managed_by_alembic': True}
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users_delegate')
