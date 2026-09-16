"""Tabla parametrización columnas tdr

Revision ID: 8db3d3eda5e3
Revises: 688bd1f97b40
Create Date: 2026-09-16 13:37:34.219813

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8db3d3eda5e3'
down_revision: Union[str, Sequence[str], None] = '688bd1f97b40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
            CREATE TABLE IF NOT EXISTS map_columns_terms_reference
            (
                map_columns_terms_reference_id serial NOT NULL,
                data_type_id integer,
                column_name text,
                table_name_relation text,
                column_name_relation_id text,
                column_name_description text,
                description text,
                CONSTRAINT map_columns_terms_reference_pkey PRIMARY KEY (map_columns_terms_reference_id),
                CONSTRAINT map_columns_terms_reference_data_type_id_fkey FOREIGN KEY (data_type_id)
                    REFERENCES public.data_types_terms_reference (data_type_id) MATCH SIMPLE
                    ON UPDATE NO ACTION
                    ON DELETE NO ACTION
                    NOT VALID
            );
        """)



def downgrade() -> None:
    op.execute("""
        DROP TABLE IF EXISTS map_columns_terms_reference;
    """)
