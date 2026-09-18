"""Función generar formulario dinamico

Revision ID: bc4c9fec0611
Revises: 16e656c9215f
Create Date: 2026-09-16 13:39:49.514055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc4c9fec0611'
down_revision: Union[str, Sequence[str], None] = '16e656c9215f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    op.execute("""
        CREATE OR REPLACE FUNCTION form_tdr(
            v_approval_flow integer DEFAULT '-1'::integer)
            RETURNS jsonb
            LANGUAGE 'plpgsql'
            COST 100
            VOLATILE PARALLEL UNSAFE
        AS $BODY$

        DECLARE
            formulario jsonb := '[]'::jsonb;
            campo RECORD;
            opciones jsonb;

        BEGIN

            FOR campo IN
                SELECT
                    a.visible,
                    b.map_columns_terms_reference_id,
                    b.column_name,
                    b.description,
                    b.table_name_relation,
                    b.column_name_description,
                    b.column_name_relation_id,
                    c.data_type

                FROM approval_flows_terms_reference_columns a

                INNER JOIN map_columns_terms_reference b
                    ON a.map_columns_terms_reference_id =
                    b.map_columns_terms_reference_id

                INNER JOIN data_types_terms_reference c
                    ON b.data_type_id = c.data_type_id

                WHERE a.approval_flow_id = v_approval_flow 
                and a.visible = true

                ORDER BY b.map_columns_terms_reference_id
            LOOP

            
                opciones := '[]'::jsonb;

                --obtener opciones

                IF campo.table_name_relation IS NOT NULL
                AND campo.table_name_relation <> ''
                AND campo.column_name_relation_id IS NOT NULL
                AND campo.column_name_description IS NOT NULL
                THEN

                    EXECUTE format(
                        '
                        SELECT COALESCE(
                            jsonb_agg(
                                jsonb_build_object(
                                    ''value'', %I,
                                    ''label'', %I
                                )
                                ORDER BY %I
                            ),
                            ''[]''::jsonb
                        )
                        FROM %I
                        ',
                        campo.column_name_relation_id,
                        campo.column_name_description,
                        campo.column_name_description,
                        campo.table_name_relation
                    )
                    INTO opciones;

                END IF;

                -- Tipo de campo BOOLEAN / LÓGICO si/no true/false
                
                IF lower(campo.data_type) IN (
                    'boolean',
                    'bool',
                    'logico',
                    'lógico',
                    'si/no',
                    'sí/no'
                )
                THEN

                    opciones := jsonb_build_array(
                        jsonb_build_object(
                            'value', true,
                            'label', 'Sí'
                        ),
                        jsonb_build_object(
                            'value', false,
                            'label', 'No'
                        )
                    );

                END IF;
                
                --Define Formulario
                
                formulario := formulario || jsonb_build_array(

                    jsonb_build_object(

                        'id',
                            campo.map_columns_terms_reference_id,

                        'name',
                            campo.column_name,

                        'label',
                            campo.description,

                        'type',
                            CASE
                                --Identifica tipo de dato
                                WHEN lower(campo.data_type) IN (
                                    'boolean',
                                    'bool',
                                    'logico',
                                    'lógico',
                                    'si/no',
                                    'sí/no'
                                )
                                THEN 'radio'

                                WHEN lower(campo.data_type) = 'seleccion'
                                THEN 'select'

                                WHEN lower(campo.data_type) = 'texto'
                                THEN 'text'

                                WHEN lower(campo.data_type) = 'wysiwyg'
                                THEN 'wysiwyg'

                                WHEN lower(campo.data_type) IN (
                                    'numero',
                                    'número'
                                )
                                THEN 'number'

                                WHEN lower(campo.data_type) = 'fecha'
                                THEN 'date'

                                WHEN lower(campo.data_type) = 'textarea'
                                THEN 'textarea'

                                WHEN lower(campo.data_type) = 'checkbox'
                                THEN 'checkbox'

                                WHEN lower(campo.data_type) = 'radio'
                                THEN 'radio'

                                --por defecto
                                ELSE 'text'

                            END,

                        --Propiedades
                        'visible',
                            COALESCE(campo.visible, true),

                        'required',
                            false,

                        'disabled',
                            false,

                        --opciones
                        'options',
                            opciones
                    )
                );

            END LOOP;

            RETURN jsonb_build_object(
                'form',
                jsonb_build_object(
                    'name', 'TDR',
                    'fields', formulario
                )
            );

        END;

        $BODY$;

    """)


def downgrade():
    op.execute("""
    DROP FUNCTION IF EXISTS form_tdr;
    """)