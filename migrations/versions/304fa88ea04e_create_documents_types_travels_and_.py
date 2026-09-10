"""create_documents_types_travels_and_update_attachments

Revision ID: 304fa88ea04e
Revises: d4b8e21a9c37
Create Date: 2026-09-10 12:22:55.850147

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '304fa88ea04e'
down_revision: Union[str, Sequence[str], None] = 'd4b8e21a9c37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Crear la tabla documents_types_travels
    op.create_table(
        'documents_types_travels',
        sa.Column('document_type_id', sa.Integer(), nullable=False),
        sa.Column('document_category', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('document_type_id')
    )

    # Insertar data semilla
    op.execute(
        "INSERT INTO documents_types_travels (document_type_id, document_category) VALUES "
        "(1, 'Facturas'), "
        "(2, 'Documentos Relacionados')"
    )

    # Modificar la tabla attachment_travel_tp
    op.add_column('attachment_travel_tp', sa.Column('observations', sa.Text(), nullable=True))
    op.add_column('attachment_travel_tp', sa.Column('document_type_id', sa.Integer(), nullable=True))
    
    # Crear foreign key
    op.create_foreign_key(
        'fk_attachment_travel_tp_doc_type',
        'attachment_travel_tp',
        'documents_types_travels',
        ['document_type_id'],
        ['document_type_id']
    )


def downgrade() -> None:
    # Revertir cambios en attachment_travel_tp
    op.drop_constraint('fk_attachment_travel_tp_doc_type', 'attachment_travel_tp', type_='foreignkey')
    op.drop_column('attachment_travel_tp', 'document_type_id')
    op.drop_column('attachment_travel_tp', 'observations')

    # Eliminar la tabla documents_types_travels
    op.drop_table('documents_types_travels')
