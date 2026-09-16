"""Función insertar campos dinamicos

Revision ID: ba03ea7600b5
Revises: bc4c9fec0611
Create Date: 2026-09-16 13:44:04.924089

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba03ea7600b5'
down_revision: Union[str, Sequence[str], None] = 'bc4c9fec0611'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
            CREATE OR REPLACE FUNCTION public.insert_terms_reference(
                p_program_id integer,
                p_description text,
                p_approval_flow_id integer,
                p_created_by_user_id integer,
                p_status_id integer,
                p_tdr_form jsonb)
                RETURNS jsonb
                LANGUAGE 'plpgsql'
                COST 100
                VOLATILE PARALLEL UNSAFE
            AS $BODY$

            DECLARE
                v_terms_reference_id integer;

                v_columns text := '';
                v_values text := '';

                v_field RECORD;
                v_column RECORD;
                v_sql text;

                v_first boolean := true;

            BEGIN

                -- Validar APPROVAL FLOW

                IF NOT EXISTS (
                    SELECT 1
                    FROM approval_flows
                    WHERE approval_flow_id = p_approval_flow_id
                ) THEN

                    RAISE EXCEPTION
                        'El approval_flow_id % no existe',
                        p_approval_flow_id;

                END IF;

                -- Validar que tdr_form sea un arreglo JSON

                IF p_tdr_form IS NULL
                OR jsonb_typeof(p_tdr_form) <> 'array'
                THEN

                    RAISE EXCEPTION
                        'p_tdr_form debe ser un arreglo JSON';

                END IF;

                -- Recorrer los campos enviados

                FOR v_field IN

                    SELECT
                        (item->>'id')::integer AS map_columns_terms_reference_id,
                        item->'value' AS value

                    FROM jsonb_array_elements(p_tdr_form) AS item

                LOOP


                    IF v_field.map_columns_terms_reference_id IS NULL THEN

                        RAISE EXCEPTION
                            'Todos los campos del formulario deben tener id';

                    END IF;

                    -- Buscar la columna configurada

                    SELECT
                        mc.column_name,
                        mc.data_type_id

                    INTO v_column

                    FROM approval_flows_terms_reference_columns af

                    INNER JOIN map_columns_terms_reference mc
                        ON mc.map_columns_terms_reference_id =
                        af.map_columns_terms_reference_id

                    WHERE af.approval_flow_id = p_approval_flow_id

                    AND af.map_columns_terms_reference_id =
                        v_field.map_columns_terms_reference_id;


                    IF NOT FOUND THEN

                        RAISE EXCEPTION
                            'El campo % no está configurado para el approval_flow_id %',
                            v_field.map_columns_terms_reference_id,
                            p_approval_flow_id;

                    END IF;


                    IF NOT EXISTS (

                        SELECT 1

                        FROM information_schema.columns c

                        WHERE 
                        
                        c.table_name = 'terms_reference'

                        AND c.column_name = v_column.column_name

                    ) THEN

                        RAISE EXCEPTION
                            'La columna "%" no existe en terms_reference',
                            v_column.column_name;

                    END IF;

                    -- Evitar columnas duplicadas

                    IF v_columns <> ''

                    AND v_columns ~
                        format(
                            r'(^|,\s*)"?%s"?(\s*,|$)',
                            regexp_replace(
                                v_column.column_name,
                                r'([\.^$|()\[\]{}*+?])',
                                r'\\\1',
                                'g'
                            )
                        )

                    THEN

                        RAISE EXCEPTION
                            'El campo "%" fue enviado más de una vez',
                            v_column.column_name;

                    END IF;

                    -- Agregar columna

                    IF NOT v_first THEN

                        v_columns := v_columns || ', ';
                        v_values := v_values || ', ';

                    END IF;

                    v_first := false;

                    v_columns := v_columns ||
                        format('%I', v_column.column_name);

                    -- Agregar valor de la columna

                    IF v_field.value IS NULL
                    OR v_field.value = 'null'::jsonb
                    THEN

                        v_values := v_values || 'NULL';

                    ELSE

                        -- Detectar tipo de dato

                        SELECT
                            c.data_type,
                            c.udt_name

                        INTO v_column

                        FROM information_schema.columns c

                        WHERE 
                        c.table_name = 'terms_reference'

                        AND c.column_name = v_column.column_name;


                        IF v_column.udt_name IN (
                            'int2',
                            'int4',
                            'int8'
                        )
                        THEN

                            v_values := v_values ||
                                format(
                                    '%L::%s',
                                    v_field.value->>'value',
                                    v_column.udt_name
                                );


                        ELSIF v_column.udt_name = 'bool'
                        THEN

                            v_values := v_values ||
                                format(
                                    '%L::boolean',
                                    v_field.value->>'value'
                                );


                        ELSIF v_column.udt_name = 'uuid'
                        THEN

                            v_values := v_values ||
                                format(
                                    '%L::uuid',
                                    v_field.value->>'value'
                                );


                        ELSIF v_column.udt_name IN (
                            'numeric',
                            'float4',
                            'float8'
                        )
                        THEN

                            v_values := v_values ||
                                format(
                                    '%L::%s',
                                    v_field.value->>'value',
                                    v_column.udt_name
                                );


                        ELSE

                            v_values := v_values ||
                                format(
                                    '%L',
                                    v_field.value->>'value'
                                );

                        END IF;

                    END IF;

                END LOOP;

                -- Construir el insert

                v_sql := format(
                    '
                    INSERT INTO terms_reference
                    (
                        program_id,
                        approval_flow_id,
                        description,
                        created_by_user_id,
                        created_at%s
                    )
                    VALUES
                    (
                        %L,
                        %L,
                        %L,
                        %L,
                        NOW()%s
                    )
                    RETURNING terms_reference_id
                    ',

                    CASE
                        WHEN v_columns <> ''
                        THEN ', ' || v_columns
                        ELSE ''
                    END,

                    p_program_id,
                    p_approval_flow_id,
                    p_description,
                    p_created_by_user_id,
                    CASE
                        WHEN v_values <> ''
                        THEN ', ' || v_values
                        ELSE ''
                    END
                );

                -- Ejecutar el insert

                EXECUTE v_sql
                INTO v_terms_reference_id;

                -- Retornar el ID

                RETURN jsonb_build_object(

                    'solicitud_exitosa', true,

                    'mensaje',
                        'TDR creada correctamente',

                    'identity',
                        v_terms_reference_id

                );

            END;

            $BODY$;

    """)


def downgrade():
    op.execute("""
    DROP FUNCTION IF EXISTS insert_dynamic_fields;
    """)