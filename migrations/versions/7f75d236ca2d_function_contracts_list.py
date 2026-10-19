"""function_contracts_list

Revision ID: 7f75d236ca2d
Revises: 2d4b686d5b8d
Create Date: 2026-10-19 09:34:50.120289

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f75d236ca2d'
down_revision: Union[str, Sequence[str], None] = '2d4b686d5b8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
              DROP FUNCTION IF EXISTS public.list_contracts
          """)


    op.execute("""   
               
    CREATE OR REPLACE FUNCTION public.list_contracts(
    page        integer           DEFAULT 1,      -- Página (-1 = sin paginación)
    filter      character varying DEFAULT '',     -- Búsqueda por código
    v_year      integer           DEFAULT -1,     -- Año (-1 = todos)
    v_type      integer           DEFAULT -1,     -- tipo de contrato (-1 = todas)
    v_parent_id bigint            DEFAULT -1      -- -1 = solo contratos padre o id jiho
)
RETURNS TABLE(
    id                       bigint,
    code                     text,
    description              text,
    line_paa                 integer,
    line_pad                 integer,
    year                     integer,
    start_contract_date      date,
    end_contract_date        date,
    bank_code                text,
    address_line_1           text,
    address_line_2           text,
    mobile_phone             text,
    program_name             text,
    is_currency_usd          boolean,
    contract_type_name       text,
    pillar_name              text,
    expense_category_name    text,
    purchase_type_name       text,
    observations             text,
    created_at               timestamp,
    updated_at               timestamp,
    policy_approval          boolean,
    policy_date              date,
    final_date               date,
    early_settlement_date    date,
    causes_early_termination text,
    released_resource        numeric,
    value                    numeric,
    total_adition            numeric,
    last_dibursement         numeric,
    dibursement_value        numeric,
    accumulated_value        numeric,
    settle_value             numeric,
    remaining_value          numeric,
    total_restante           numeric,
    can_delete               boolean,

    -- total genrak
    grand_released_resource  numeric,
    grand_value              numeric,
    grand_total_adition      numeric,
    grand_dibursement_value  numeric,
    grand_accumulated_value  numeric,
    grand_settle_value       numeric,
    grand_remaining_value    numeric,
    grand_total_restante     numeric,
    total_records            bigint,      

    -- Subt 
    page_released_resource   numeric,
    page_value               numeric,
    page_total_adition       numeric,
    page_dibursement_value   numeric,
    page_accumulated_value   numeric,
    page_settle_value        numeric,
    page_remaining_value     numeric,
    page_total_restante      numeric
)
LANGUAGE plpgsql
AS $BODY$
DECLARE
    v_offset INT;
    v_filter TEXT;
BEGIN

    v_offset := (GREATEST(page, 1) - 1) * 20;
    v_filter := TRIM(COALESCE(filter, ''));

    RAISE NOTICE 'Filtros -> page: %, filter: %, year: %, type: %, parent: %',
        page, v_filter, v_year, v_type, v_parent_id;

    RETURN QUERY
    SELECT
        m.*,

        -- Subt
        SUM(m.released_resource) OVER () AS page_released_resource,
        SUM(m.value)             OVER () AS page_value,
        SUM(m.total_adition)     OVER () AS page_total_adition,
        SUM(m.dibursement_value) OVER () AS page_dibursement_value,
        SUM(m.accumulated_value) OVER () AS page_accumulated_value,
        SUM(m.settle_value)      OVER () AS page_settle_value,
        SUM(m.remaining_value)   OVER () AS page_remaining_value,
        SUM(m.total_restante)    OVER () AS page_total_restante

    FROM (
        SELECT
            b.*,

            
            g.grand_released_resource,
            g.grand_value,
            g.grand_total_adition,
            g.grand_dibursement_value,
            g.grand_accumulated_value,
            g.grand_settle_value,
            g.grand_remaining_value,
            g.grand_total_restante,

            
            COUNT(*) OVER () AS total_records

        FROM (
            SELECT
                c.id::bigint                                    AS id,
                c.code::text                                    AS code,
                c.description::text                             AS description,
                COALESCE(lc.lines_paa, 0)::integer              AS line_paa,
                COALESCE(aq.lines_pad, 0)::integer              AS line_pad,
                c.year::integer                                 AS year,
                c.start_contract_date::date                     AS start_contract_date,
                c.end_contract_date::date                       AS end_contract_date,
                c.bank_code::text                               AS bank_code,
                c.address_line_1::text                          AS address_line_1,
                c.address_line_2::text                          AS address_line_2,
                c.mobile_phone::text                            AS mobile_phone,
                pr.name::text                                   AS program_name,
                COALESCE(c.is_currency_usd, false)::boolean     AS is_currency_usd,
                (COALESCE(ct.description, '') || ' - ' || COALESCE(ct.code, ''))::text
                                                                AS contract_type_name,
                pi.name::text                                   AS pillar_name,
                ec.name::text                                   AS expense_category_name,
                pt.name::text                                   AS purchase_type_name,
                c.observations::text                            AS observations,
                c.created_at::timestamp                         AS created_at,
                c.updated_at::timestamp                         AS updated_at,
                COALESCE(c.policy_approval, false)::boolean     AS policy_approval,
                c.policy_date::date                             AS policy_date,
                c.final_date::date                              AS final_date,
                c.early_settlement_date::date                   AS early_settlement_date,
                c.causes_early_termination::text                AS causes_early_termination,
                COALESCE(c.released_resource, 0)::numeric       AS released_resource,
                COALESCE(c.initial_value, c.value, 0)::numeric  AS value,
                COALESCE(c.total_adition, 0)::numeric           AS total_adition,
                COALESCE(c.last_dibursement, 0)::numeric        AS last_dibursement,
                COALESCE(c.dibursement_value, 0)::numeric       AS dibursement_value,
                COALESCE(c.accumulated_value, 0)::numeric       AS accumulated_value,
                COALESCE(lc.settle_value, 0)::numeric           AS settle_value,
                COALESCE(c.remaining_value, 0)::numeric         AS remaining_value,
                (CASE WHEN COALESCE(c.remaining_value, 0) > 0
                      THEN COALESCE(c.accumulated_value, 0) + c.remaining_value
                      ELSE 0
                 END)::numeric                                  AS total_restante,
                (COALESCE(lc.lines_paa, 0) = 0
                 AND NOT EXISTS (SELECT 1 FROM acquisition_contract x WHERE x.contract_id = c.id)
                 AND NOT EXISTS (SELECT 1 FROM contract_person x      WHERE x.contract_id = c.id)
                )::boolean                                      AS can_delete

            FROM contracts c
            LEFT JOIN programs           pr ON pr.id = c.program_id
            LEFT JOIN contract_types     ct ON ct.id = c.contract_type_id
            LEFT JOIN pillars            pi ON pi.id = c.pillar_id
            LEFT JOIN expense_categories ec ON ec.id = c.expense_category_id
            LEFT JOIN purchase_types     pt ON pt.id = c.purchase_type_id
            LEFT JOIN LATERAL (
                SELECT COUNT(*)            AS lines_paa,
                       SUM(l.settle_value) AS settle_value
                FROM contract_line l
                WHERE l.contract_id = c.id
            ) lc ON true
            LEFT JOIN LATERAL (
                SELECT COUNT(*) AS lines_pad
                FROM acquisitions a
                WHERE a.contractt_id = c.id
            ) aq ON true

            -- Filtros
            WHERE COALESCE(c.code, '') NOT LIKE 'OT-P-%'                        -- Sin otrosí
              AND ((v_parent_id = -1 AND c.contract_id IS NULL)                 -- padres
                   OR c.contract_id = v_parent_id)                              --  hijos
              AND (v_type      = -1 OR c.contract_type_id = v_type)             -- tipo
              AND (v_year      = -1 OR c.year             = v_year)             -- Año
              AND (v_filter    = '' OR c.code ILIKE '%' || v_filter || '%')     -- Código
        ) b

        -- total gnar
        CROSS JOIN (
            SELECT
                SUM(COALESCE(c2.released_resource, 0))::numeric           AS grand_released_resource,
                SUM(COALESCE(c2.initial_value, c2.value, 0))::numeric     AS grand_value,
                SUM(COALESCE(c2.total_adition, 0))::numeric               AS grand_total_adition,
                SUM(COALESCE(c2.dibursement_value, 0))::numeric           AS grand_dibursement_value,
                SUM(COALESCE(c2.accumulated_value, 0))::numeric           AS grand_accumulated_value,
                SUM(COALESCE(lc2.settle_value, 0))::numeric               AS grand_settle_value,
                SUM(COALESCE(c2.remaining_value, 0))::numeric             AS grand_remaining_value,
                SUM(CASE WHEN COALESCE(c2.remaining_value, 0) > 0
                         THEN COALESCE(c2.accumulated_value, 0) + c2.remaining_value
                         ELSE 0
                    END)::numeric                                         AS grand_total_restante
            FROM contracts c2
            LEFT JOIN LATERAL (
                SELECT SUM(l.settle_value) AS settle_value
                FROM contract_line l
                WHERE l.contract_id = c2.id
            ) lc2 ON true
            WHERE c2.contract_id IS NULL                       -- Solo contratos padre
              AND COALESCE(c2.code, '') NOT LIKE 'OT-P-%'      -- Sin otrosí
        ) g

        ORDER BY b.id DESC
        LIMIT  CASE WHEN page = -1 THEN NULL ELSE 20       END
        OFFSET CASE WHEN page = -1 THEN 0    ELSE v_offset END
    ) m
    ORDER BY m.id DESC;
END;
$BODY$;
               
      
               """)