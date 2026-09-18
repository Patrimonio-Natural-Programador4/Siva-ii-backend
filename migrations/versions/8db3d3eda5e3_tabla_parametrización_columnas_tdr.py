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
            CREATE TABLE IF NOT EXISTS data_types_terms_reference
            (
                data_type_id serial NOT NULL,
                data_type text,
                CONSTRAINT data_types_terms_reference_pkey PRIMARY KEY (data_type_id)
            );

            INSERT INTO data_types_terms_reference (data_type)
            SELECT t.data_type FROM (VALUES
                ('texto'),
                ('numero'),
                ('fecha'),
                ('boolean'),
                ('seleccion'),
                ('textarea'),
                ('wysiwyg'),
                ('checkbox'),
                ('radio')
            ) AS t(data_type)
            WHERE NOT EXISTS (
                SELECT 1 FROM data_types_terms_reference WHERE data_types_terms_reference.data_type = t.data_type
            );

            CREATE TABLE IF NOT EXISTS terms_reference_status
            (
                status_id serial NOT NULL,
                status text NOT NULL,
                CONSTRAINT terms_reference_status_pkey PRIMARY KEY (status_id)
            );

            CREATE TABLE IF NOT EXISTS terms_reference
            (
                terms_reference_id serial NOT NULL,
                guid uuid DEFAULT gen_random_uuid(),
                rubro_id integer,
                pid_id integer,
                expense_categories_id integer,
                selection_procedure_id integer,
                activity_id integer,
                evaluation_method_id integer,
                object text,
                process_number text,
                scope text,
                execution_period text,
                place_execution text,
                supervisor_id integer,
                educational_background text,
                general_professional_experience text,
                name text,
                description text,
                program_id integer,
                approval_request_id integer,
                created_by_user_id integer,
                created_at timestamp with time zone DEFAULT now(),
                status_id integer,
                approval_flow_id integer,
                CONSTRAINT terms_reference_pkey PRIMARY KEY (terms_reference_id)
            );

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
        DROP TABLE IF EXISTS terms_reference;
        DROP TABLE IF EXISTS terms_reference_status;
        DROP TABLE IF EXISTS data_types_terms_reference;
    """)
