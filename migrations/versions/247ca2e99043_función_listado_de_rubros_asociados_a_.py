"""Función listado de rubros asociados a costos operativos

Revision ID: 247ca2e99043
Revises: bda72b876987
Create Date: 2026-08-06 15:00:36.838174

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '247ca2e99043'
down_revision: Union[str, Sequence[str], None] = 'bda72b876987'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
    CREATE OR REPLACE FUNCTION public.rubros_list(
        v_year character varying DEFAULT ''::character varying
    )
    RETURNS TABLE(
        rubro_id bigint,
        rubros text,
        short_rubro text,
        activity_id bigint,
        activity_code text,
        activity_description text
    )
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000
    AS $BODY$
    BEGIN
        RETURN QUERY
        SELECT
            a.rubro_id,
            c.rubros::text,
            (json_rubros::jsonb)->0->'rubros'->>v_year AS short_rubro,
            a.activity_id,
            b.code::text AS activity_code,
            b.description::text AS activity_description
        FROM acquisitions a
        INNER JOIN activities b 
            ON a.activity_id = b.id 
           AND b.is_logistics_expense_associate = true
        INNER JOIN rubros c 
            ON a.rubro_id = c.id
        WHERE COALESCE((json_rubros::jsonb)->0->'rubros'->>v_year, '') <> '';
    END;
    $BODY$;
    """)


def downgrade():
    op.execute("""
    DROP FUNCTION IF EXISTS public.rubros_list(character varying);
    """)