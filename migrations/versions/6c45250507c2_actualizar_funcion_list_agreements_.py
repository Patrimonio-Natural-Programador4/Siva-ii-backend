"""actualizar_funcion_list_agreements_filtros

Revision ID: 6c45250507c2
Revises: 543a08cb0cce
Create Date: 2026-10-09 00:08:44.240000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c45250507c2'
down_revision: Union[str, Sequence[str], None] = '543a08cb0cce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
    DROP FUNCTION IF EXISTS list_agreements(
        integer, integer[], integer[], integer[], integer[], 
        integer[], text[], integer[], text[], text[], text, integer, integer
    );
    DROP FUNCTION IF EXISTS list_agreements(
        integer, integer[], integer[], integer[], integer[], 
        integer[], character varying[], integer[], character varying[], character varying[], character varying, integer, integer
    );

    CREATE OR REPLACE FUNCTION list_agreements(
        p_agreement_id INTEGER DEFAULT NULL,
        p_type_ids INTEGER[] DEFAULT NULL,
        p_modality_ids INTEGER[] DEFAULT NULL,
        p_pillar_ids INTEGER[] DEFAULT NULL,
        p_core_ids INTEGER[] DEFAULT NULL,
        p_years INTEGER[] DEFAULT NULL,
        p_phase VARCHAR[] DEFAULT NULL,
        p_stage_ids INTEGER[] DEFAULT NULL,
        p_priority VARCHAR[] DEFAULT NULL,
        p_alert VARCHAR[] DEFAULT NULL,
        p_search VARCHAR DEFAULT NULL,
        p_page INTEGER DEFAULT 1,
        p_page_size INTEGER DEFAULT 20
    )
    RETURNS TABLE (
        id INTEGER,
        codigo_siva VARCHAR,
        nombre_convenio VARCHAR,
        objeto_acuerdo VARCHAR,
        prioridad_acuerdo VARCHAR,
        ano_ejecucion INTEGER,
        estado_name VARCHAR,
        estado_stage VARCHAR,
        estado_status VARCHAR,
        estado_color VARCHAR,
        tipo_name VARCHAR,
        tipo_color VARCHAR,
        modalidad_name VARCHAR,
        pilar_name VARCHAR,
        pilar_color VARCHAR,
        nucleos TEXT,
        implementadoras TEXT,
        monto_apropiado NUMERIC,
        monto_total_apropiado NUMERIC,
        total_paa NUMERIC,
        total_records INTEGER
    ) 
    LANGUAGE plpgsql
    AS $$
    BEGIN

        RETURN QUERY 
        WITH filtered_agreements AS (
            SELECT 
                a.id,
                a.code AS codigo_siva,
                a.name AS nombre_convenio,
                a.description AS objeto_acuerdo,
                a.priority AS prioridad_acuerdo,
                a.year AS ano_ejecucion,
                ast.name AS estado_name,
                ast.stage AS estado_stage,
                ast.status AS estado_status,
                ast.color AS estado_color,
                aty.name AS tipo_name,
                aty.color AS tipo_color,
                m.name AS modalidad_name,
                p.name AS pilar_name,
                p.color AS pilar_color,
                a.value::NUMERIC AS monto_apropiado,
                a.value::NUMERIC AS monto_total_apropiado,
                0::NUMERIC AS total_paa,
                COUNT(*) OVER()::INTEGER AS total_records 
            FROM 
                agreements a
            LEFT JOIN agreement_stages ast ON a.agreement_stage_id = ast.id
            LEFT JOIN agreement_types aty ON a.agreement_type_id = aty.id
            LEFT JOIN modalities m ON a.modality_id = m.id
            LEFT JOIN pillars p ON a.pillar_id = p.id
            WHERE 
                (a.agreement_id IS NULL OR aty.is_independent = true)
                AND (p_agreement_id IS NULL OR a.id = p_agreement_id)
                AND (COALESCE(cardinality(p_type_ids), 0) = 0 OR a.agreement_type_id = ANY(p_type_ids) OR (0 = ANY(p_type_ids) AND a.agreement_type_id IS NULL))
                AND (COALESCE(cardinality(p_modality_ids), 0) = 0 OR a.modality_id = ANY(p_modality_ids))
                AND (COALESCE(cardinality(p_pillar_ids), 0) = 0 OR a.pillar_id = ANY(p_pillar_ids))
                AND (COALESCE(cardinality(p_years), 0) = 0 OR a.year = ANY(p_years))
                AND (COALESCE(cardinality(p_stage_ids), 0) = 0 OR a.agreement_stage_id = ANY(p_stage_ids))
                AND (COALESCE(cardinality(p_phase), 0) = 0 OR ast.name = ANY(p_phase) OR ast.stage = ANY(p_phase))
                AND (COALESCE(cardinality(p_priority), 0) = 0 OR a.priority = ANY(p_priority))
                AND (COALESCE(cardinality(p_alert), 0) = 0 OR 
                     ('Sin Alerta' = ANY(p_alert) AND a.alert IS NULL) OR 
                     a.alert = ANY(p_alert))
                
                AND (COALESCE(cardinality(p_core_ids), 0) = 0 OR EXISTS (
                      SELECT 1 FROM agreements_core ac 
                      WHERE ac.agreement_id = a.id AND ac.core_id = ANY(p_core_ids)
                ))
                
                AND (p_search IS NULL OR p_search = '' OR 
                     a.name ILIKE '%' || p_search || '%' OR 
                     a.code ILIKE '%' || p_search || '%' OR
                     a.description ILIKE '%' || p_search || '%')
            ORDER BY a.id ASC
            LIMIT p_page_size
            OFFSET (p_page - 1) * p_page_size
        )
        SELECT 
            fa.id::INTEGER,
            fa.codigo_siva::VARCHAR,
            fa.nombre_convenio::VARCHAR,
            fa.objeto_acuerdo::VARCHAR,
            fa.prioridad_acuerdo::VARCHAR,
            fa.ano_ejecucion::INTEGER,
            fa.estado_name::VARCHAR,
            fa.estado_stage::VARCHAR,
            fa.estado_status::VARCHAR,
            fa.estado_color::VARCHAR,
            fa.tipo_name::VARCHAR,
            fa.tipo_color::VARCHAR,
            fa.modalidad_name::VARCHAR,
            fa.pilar_name::VARCHAR,
            fa.pilar_color::VARCHAR,
            
            (SELECT string_agg(c.core_name, ', ') 
             FROM agreements_core ac 
             JOIN core_category c ON ac.core_id = c.id 
             WHERE ac.agreement_id = fa.id) AS nucleos,
             
            (SELECT string_agg(COALESCE(NULLIF(i.acronym, ''), i.name), ', ') 
             FROM agreement_implementer ai 
             JOIN implementers i ON ai.implementer_id = i.id 
             WHERE ai.agreement_id = fa.id) AS implementadoras,
             
            fa.monto_apropiado::NUMERIC,
            fa.monto_total_apropiado::NUMERIC,
            fa.total_paa::NUMERIC,
            fa.total_records::INTEGER
        FROM 
            filtered_agreements fa
        ORDER BY 
            fa.id ASC;

    END;
    $$;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
    DROP FUNCTION IF EXISTS list_agreements(
        integer, integer[], integer[], integer[], integer[], 
        integer[], character varying[], integer[], character varying[], character varying[], character varying, integer, integer
    );
    """)
