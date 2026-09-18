"""Tabla configuración TDR Columnas dinamicas

Revision ID: 16e656c9215f
Revises: 8db3d3eda5e3
Create Date: 2026-09-16 13:38:37.956700

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16e656c9215f'
down_revision: Union[str, Sequence[str], None] = '8db3d3eda5e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
            CREATE TABLE IF NOT EXISTS approval_flows_terms_reference_columns
            (
                approval_flows_terms_reference_columns_id serial NOT NULL,
                map_columns_terms_reference_id integer,
                approval_flow_id integer,
                visible boolean,
                CONSTRAINT approval_flows_terms_reference_columns_pkey PRIMARY KEY (approval_flows_terms_reference_columns_id),
                CONSTRAINT approval_flows_terms_referenc_map_columns_terms_reference_fkey FOREIGN KEY (map_columns_terms_reference_id)
                    REFERENCES public.map_columns_terms_reference (map_columns_terms_reference_id) MATCH SIMPLE
                    ON UPDATE NO ACTION
                    ON DELETE NO ACTION,
                CONSTRAINT approval_flows_terms_reference_columns_approval_flow_id_fkey FOREIGN KEY (approval_flow_id)
                    REFERENCES public.approval_flows (approval_flow_id) MATCH SIMPLE
                    ON UPDATE NO ACTION
                    ON DELETE NO ACTION
            );
        """)



def downgrade() -> None:
    op.execute("""
        DROP TABLE IF EXISTS approval_flows_terms_reference_columns;
    """)
