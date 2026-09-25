"""Crear función List agreements

Revision ID: 85306d2e3ece
Revises: 028b227fa2db
Create Date: 2026-09-23 15:51:04.790694

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85306d2e3ece'
down_revision: Union[str, Sequence[str], None] = '028b227fa2db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
    CREATE OR REPLACE FUNCTION public.list_agreements(
    p_agreement_id integer DEFAULT NULL,     -- id puntual (detalle, ej. list_agreements(7))
    p_type_ids integer[] DEFAULT NULL,       -- Filtrar por tipo
    p_modality_ids integer[] DEFAULT NULL,   -- Filtrar por modalidad
    p_core_ids integer[] DEFAULT NULL,       -- Filtrar por núcleo
    p_pillar_ids integer[] DEFAULT NULL,     -- Filtrar por pilar
    p_years integer[] DEFAULT NULL,          -- Filtrar por años
    p_phase text[] DEFAULT NULL,             -- Filtrar por Fase (agreement_stages.name)
    p_stage_ids integer[] DEFAULT NULL,      -- Filtrar por estado (agreement_stage_id puntual)
    p_priority text[] DEFAULT NULL,          -- Filtrar por prioridad: 'Alto','Medio','Bajo','0'(=NULL)
    p_alert text[] DEFAULT NULL,             -- Filtrar por Alerta Vigencia: 'Alta','Media','Baja','Sin Alerta'(=NULL)
    p_search text DEFAULT NULL,              -- Buscar implementadora | Código
    p_page integer DEFAULT 1,
    p_page_size integer DEFAULT 25           -- 25 por página, según "Showing 1 to 25 of 118 results"
)
RETURNS TABLE (
    id bigint,
    codigo_siva character varying,
    nombre_convenio citext,
    objeto_acuerdo citext,
    prioridad_acuerdo character varying,
    ano_ejecucion integer,
    estado_name character varying,
    estado_stage text,
    estado_status character varying,
    estado_color character varying,
    tipo_name citext,
    tipo_color character varying,
    modalidad_name character varying,
    pilar_name citext,
    pilar_color character varying,
    nucleos text,
    implementadoras text,
    monto_apropiado numeric,
    monto_total_apropiado numeric,
    total_paa numeric,
    total_records bigint
)
LANGUAGE plpgsql
AS $BODY$
BEGIN
    RETURN QUERY

    -- ============================================================
    -- BLOQUE 1: ATRIBUTOS PRINCIPALES Y RELACIONES DIRECTAS
    -- ============================================================
    SELECT
        a.id::bigint AS id,
        a.code::character varying AS codigo_siva,
        a.name::citext AS nombre_convenio,
        a.description::citext AS objeto_acuerdo,
        a.priority::character varying AS prioridad_acuerdo,
        a.year::integer AS ano_ejecucion,
        ast.name::character varying AS estado_name,
        ast.stage::text AS estado_stage,
        ast.status::character varying AS estado_status,
        ast.color::character varying AS estado_color,
        aty.name::citext AS tipo_name,
        aty.color::character varying AS tipo_color,
        m.name::character varying AS modalidad_name,
        pl.name::citext AS pilar_name,
        pl.color::character varying AS pilar_color,

        -- ============================================================
        -- BLOQUE 2: AGREGACIÓN DE NÚCLEOS Y PORCENTAJES
        -- ============================================================
        (SELECT string_agg(cc.core_name || ' (' || COALESCE(ac.porcentages_core::text, '0') || '%)', ', '
                           ORDER BY cc.core_name ASC)
         FROM agreements_core ac
         JOIN core_category cc ON cc.id = ac.core_id
         WHERE ac.agreement_id = a.id)::text AS nucleos,

        -- ============================================================
        -- BLOQUE 3: AGREGACIÓN DE ENTIDADES IMPLEMENTADORAS
        -- ============================================================
        (SELECT string_agg(i.acronym || CASE
                                           WHEN ai.is_leading THEN ' (líder)'
                                           ELSE ''
                                       END || COALESCE(' [' || ai.label || ']', ''), ', '
                           ORDER BY i.acronym)
         FROM agreement_implementer ai
         JOIN implementers i ON i.id = ai.implementer_id
         WHERE ai.agreement_id = a.id)::text AS implementadoras,

        -- ============================================================
        -- BLOQUE 4: CÁLCULO DE MONTO APROPIADO (implementer_id = 96, valor interno)
        -- ============================================================
        (SELECT SUM(ai.complementary_value)
         FROM agreement_implementer ai
         WHERE ai.agreement_id = a.id
           AND ai.implementer_id = 96)::numeric AS monto_apropiado,

        -- ============================================================
        -- BLOQUE 5: CÁLCULO DE MONTO TOTAL APROPIADO -- Revisar auto referenciacion columna 2 de 3/ valores (MONTO TOTAL APROPIADO)
        -- ============================================================
        (SELECT SUM(ai.complementary_value)
         FROM agreement_implementer ai
         WHERE ai.agreement_id = a.id)::numeric AS monto_total_apropiado,

        -- ============================================================
        -- BLOQUE 6: CÁLCULO DE PAA (valor total apropiado, líneas presupuestales)
        -- ============================================================
        (SELECT SUM(l.appropriate_value)
         FROM lines l
         WHERE l.agreement_id = a.id)::numeric AS total_paa,

        -- ============================================================
        -- BLOQUE 7: TOTAL DE REGISTROS (para paginación)
        -- ============================================================
        COUNT(*) OVER()::bigint AS total_records

    -- ============================================================
    -- BLOQUE 8: ORIGEN DE DATOS Y CRUCES (JOINS)
    -- ============================================================
    FROM agreements a
    LEFT JOIN agreement_stages ast ON ast.id = a.agreement_stage_id
    LEFT JOIN agreement_types aty ON aty.id = a.agreement_type_id
    LEFT JOIN modalities m ON m.id = a.modality_id
    LEFT JOIN pillars pl ON pl.id = a.pillar_id

    -- ============================================================
    -- BLOQUE 9: FILTROS DEL LISTADO (uno por cada control de la pantalla)
    -- ============================================================
    
	--WHERE a.agreement_id is null -- Test la sumatoria de registros debe dar 118 y no 295
	where (a.agreement_id is null or aty.is_independent = true) -- Se agrego "aty.is_independent = true" para corregir cantidad de registros que coincidan 
	and (p_agreement_id IS NULL OR a.id = p_agreement_id)
	

        -- Filtrar por tipo
        AND (p_type_ids IS NULL OR a.agreement_type_id = ANY(p_type_ids))

        -- Filtrar por modalidad
        AND (p_modality_ids IS NULL OR a.modality_id = ANY(p_modality_ids))

        -- Filtrar por núcleo (tabla puente N:M — requiere EXISTS)
        AND (p_core_ids IS NULL OR EXISTS (
            SELECT 1 FROM agreements_core ac2
            WHERE ac2.agreement_id = a.id AND ac2.core_id = ANY(p_core_ids)
        ))

        -- Filtrar por pilar
        AND (p_pillar_ids IS NULL OR a.pillar_id = ANY(p_pillar_ids))

        -- Filtrar por años
        AND (p_years IS NULL OR a.year = ANY(p_years))

        -- Filtrar por Fase (nivel general: agreement_stages.name)
        AND (p_phase IS NULL OR ast.name::text = ANY(p_phase))

        -- Filtrar por estado (fila puntual: agreement_stage_id exacto)
        AND (p_stage_ids IS NULL OR a.agreement_stage_id = ANY(p_stage_ids))

        -- Filtrar por prioridad — '0' en el filtro representa priority IS NULL
        AND (p_priority IS NULL OR
             ('0' = ANY(p_priority) AND a.priority IS NULL) OR
             a.priority = ANY(p_priority))

        -- Filtrar por Alerta Vigencia — 'Sin Alerta' representa alert IS NULL
        AND (p_alert IS NULL OR
             ('Sin Alerta' = ANY(p_alert) AND a.alert IS NULL) OR
             a.alert = ANY(p_alert))

        -- Buscar implementadora | Código
        AND (p_search IS NULL OR p_search = '' OR
             a.code ILIKE '%' || p_search || '%' OR
             EXISTS (
                 SELECT 1 FROM agreement_implementer ai2
                 JOIN implementers i2 ON i2.id = ai2.implementer_id
                 WHERE ai2.agreement_id = a.id AND i2.acronym ILIKE '%' || p_search || '%'
             ))

    -- ============================================================
    -- BLOQUE 10: ORDEN Y PAGINACIÓN
    -- ============================================================
    ORDER BY a.id
    LIMIT p_page_size OFFSET (p_page - 1) * p_page_size;
END;
$BODY$; 
              
""")

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
    DROP FUNCTION IF EXISTS public.list_agreements(
        integer, integer[], integer[], integer[], integer[], 
        integer[], text[], integer[], text[], text[], text, integer, integer
    );
