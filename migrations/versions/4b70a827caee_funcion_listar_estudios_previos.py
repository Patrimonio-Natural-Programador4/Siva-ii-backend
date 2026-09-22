"""Funcion listar estudios previos

Revision ID: 4b70a827caee
Revises: e8cf13c49eee
Create Date: 2026-09-21 11:52:47.555738

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b70a827caee'
down_revision: Union[str, Sequence[str], None] = 'e8cf13c49eee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.execute("""
           DROP FUNCTION IF EXISTS public.list_previous_studies(
               character varying, integer, integer[], character varying, integer
           );
       """)
    
    
   op.execute("""
              
    CREATE OR REPLACE FUNCTION public.list_previous_studies(IN guid_user_msft character varying,IN page integer DEFAULT 1,IN v_status integer[] DEFAULT  ARRAY['-1'::integer],IN filter character varying DEFAULT  ''::character varying,IN v_program integer DEFAULT  '-1'::integer)
    RETURNS TABLE(precedents text, justification text, scope text, overall_objective text, term text, obligations text, supervisor text, total_value bigint, contributions_ei bigint, total_value_executes_fpn bigint, total_value_executes_ei bigint, previous_studies_states_id integer, implementer_id bigint, implementer_name citext, persons_id bigint, persons_email character varying, capacity_assessment_id bigint, capacity_assessment_name text, guid uuid, program_id bigint, program_name citext, contributions_fpn bigint, estimated_term text, code text, previous_studies_states_name text, pending_my_approval boolean, approval_request_id bigint, user_id bigint, guid_msft uuid, step_order_actual_request integer, guid_msft_adjustment uuid, total_records bigint)
    LANGUAGE 'plpgsql'
    VOLATILE
    PARALLEL UNSAFE
    COST 100    ROWS 1000 
    
AS $BODY$
DECLARE
    v_id_user INT;
    v_list_all_request INT;
    v_list_supervised_requests INT;
    v_offset INT;
BEGIN
    SELECT a.id INTO v_id_user
    FROM users a
    WHERE a.guid_msft = guid_user_msft::UUID;

    RAISE NOTICE 'TS: %', v_status;

    v_offset = (page - 1) * 20;

    CREATE TEMPORARY TABLE tmp_rol AS
    SELECT a.role_id
    FROM model_has_roles a
    WHERE a.model_id = v_id_user;

    CREATE TEMPORARY TABLE tmp_control AS
    SELECT b.code
    FROM control_access a
    INNER JOIN controls b ON a.control_id = b.control_id
    INNER JOIN modules c ON b.module_id = c.id
    WHERE a.role_id IN (SELECT role_id FROM tmp_rol)
    AND b.requires_validation = TRUE
    AND c.code = 'ADM_STU_PREV';

    CREATE TEMPORARY TABLE tmp_pending_records AS
    SELECT b.related_record_id
    FROM approval_request_history a
    INNER JOIN approval_requests b ON a.approval_request_id = b.approval_request_id
    INNER JOIN approval_flows c ON b.approval_workflow_id = c.approval_flow_id
    INNER JOIN approval_categories e on c.category_id = e.category_id
    WHERE a.approval_status_id = 6
    AND a.user_id = v_id_user
    AND e.code = 'APP_EP';

    INSERT INTO tmp_pending_records
    SELECT b.related_record_id
    FROM approval_request_history a
    INNER JOIN approval_requests b ON a.approval_request_id = b.approval_request_id
    INNER JOIN approval_flows c ON b.approval_workflow_id = c.approval_flow_id
    INNER JOIN approval_role_users d ON a.approval_role_id = d.approval_role_id
    INNER JOIN approval_categories e on c.category_id = e.category_id
    AND d.user_id = v_id_user
    WHERE a.approval_status_id = 6
    AND b.approval_status_id = 6
    AND d.user_id = v_id_user
    and a.user_id is null
    AND e.code = 'APP_EP';

    SELECT count(*) INTO v_list_all_request
    FROM tmp_control a
    WHERE a.code = 'TS';

    SELECT count(*) INTO v_list_supervised_requests
    FROM tmp_control a
    WHERE a.code = 'UBS';

    IF v_list_all_request > 0 THEN
        RAISE NOTICE 'Entro: %', v_list_all_request;

        RETURN QUERY
        SELECT
            v.precedents,
            v.justification,
            v.scope,
            v.overall_objective,
            v.term  ,
            v.obligations ,
            v.supervisor ,
            v.total_value ,
            v.contributions_ei ,
            v.total_value_executes_fpn ,
            v.total_value_executes_ei ,
            v.previous_studies_states_id,
            
            v.implementer_id,
            im.acronym,
            v.persons_id,
            p.email,
            v.capacity_assessment_id,
            ca.name,
            v.guid,
            v.program_id,
            c.name,
            v.contributions_fpn,
            v.estimated_term,
            v.code,
            b.state,  -- buuu
            CASE
                WHEN (v.id IN (SELECT related_record_id FROM tmp_pending_records)
                    AND v.previous_studies_states_id IN (2))
                    OR (v.previous_studies_states_id = 3
                    AND v.user_session = v_id_user) THEN true
                ELSE false
            END AS pending_my_approval,
            v.approval_request_id,
            v.user_session,
            a.guid_msft,
            CASE WHEN v.approval_request_id IS NULL THEN 0 ELSE sv.step_order END AS step_order_actual_request,
            CASE WHEN v.approval_request_id IS NULL THEN NULL ELSE sv.guid_msft_adjustment END AS guid_msft_adjustment,
            COUNT(*) OVER() AS total_records
        FROM previous_studies v
        INNER JOIN users a ON v.user_session = a.id
        INNER JOIN previous_studies_states b ON v.previous_studies_states_id = b.id
        LEFT JOIN implementers im ON v.implementer_id = im.id
        LEFT JOIN programs c ON v.program_id = c.id
        LEFT JOIN persons p ON v.persons_id = p.id
        LEFT JOIN capacity_assessments ca ON v.capacity_assessment_id = ca.id
        LEFT JOIN LATERAL (
            SELECT
                '(' || ra.name || CASE WHEN us.full_name IS NULL THEN '' ELSE ' -> ' || us.full_name END || ')' AS responsable,
                fr.step_order,
                us.guid_msft AS guid_msft_adjustment
            FROM approval_request_history hi
            INNER JOIN approval_roles ra ON hi.approval_role_id = ra.approval_role_id
            LEFT JOIN users us ON hi.user_id = us.id
            LEFT JOIN approval_flow_steps fr ON hi.step_id = fr.step_id
            WHERE v.approval_request_id = hi.approval_request_id
            ORDER BY hi.history_id DESC
            LIMIT 1
        ) sv ON TRUE
        WHERE (v_status = ARRAY[-1] OR v.previous_studies_states_id = ANY(v_status))
          AND (v.program_id = v_program OR v_program = -1)
          AND (im.acronym ILIKE '%' || filter || '%' OR v.code ILIKE '%' || filter || '%' OR filter = '')
        ORDER BY pending_my_approval DESC, v.id DESC
        LIMIT 20 OFFSET (page - 1) * 20;
    ELSE
        RAISE NOTICE 'ENTRO 2: %', v_list_all_request;

        RETURN QUERY
        SELECT
            v.precedents,
            v.justification,
            v.scope,
            v.overall_objective,
            v.term  ,
            v.obligations ,
            v.supervisor ,
            v.total_value ,
            v.contributions_ei ,
            v.total_value_executes_fpn ,
            v.total_value_executes_ei ,
            v.previous_studies_states_id,
            
            v.implementer_id,
            im.acronym,
            v.persons_id,
            p.email,
            v.capacity_assessment_id,
            ca.name,
            v.guid,
            v.program_id,
            c.name,
            v.contributions_fpn,
            v.estimated_term,
            v.code,
            b.state, -- buu
            CASE
                WHEN (v.id IN (SELECT related_record_id FROM tmp_pending_records) and v.previous_studies_states_id in (2)) or (v.previous_studies_states_id = 3 and v.user_session = v_id_user) THEN true
                ELSE false
            END AS pending_my_approval,
            v.approval_request_id,
            v.user_session,
            a.guid_msft,
            case when v.approval_request_id is null then 0 else sv.step_order end step_order_actual_request,
            case when v.approval_request_id is null then null else sv.guid_msft_adjustment end guid_msft_adjustment,
            COUNT(*) OVER() AS total_records
        FROM previous_studies v
        INNER JOIN users a ON v.user_session = a.id
        INNER JOIN previous_studies_states b ON v.previous_studies_states_id = b.id
        LEFT JOIN implementers im on v.implementer_id = im.id
        LEFT JOIN programs c on v.program_id = c.id
        LEFT JOIN persons p ON v.persons_id = p.id
        LEFT JOIN capacity_assessments ca ON v.capacity_assessment_id = ca.id
        LEFT JOIN LATERAL (
            SELECT '(' || ra.name || case when us.full_name is null then '' else ' -> ' || us.full_name end || ')' as responsable, fr.step_order,
            us.guid_msft as guid_msft_adjustment
            FROM approval_request_history hi
            inner join approval_roles ra on hi.approval_role_id = ra.approval_role_id
            left join users us on hi.user_id = us.id
            left join approval_flow_steps fr on hi.step_id = fr.step_id
            WHERE v.approval_request_id = hi.approval_request_id
            ORDER BY hi.history_id DESC
            LIMIT 1
        ) sv ON true

        WHERE v.user_session = v_id_user
        or v.id in(SELECT related_record_id FROM tmp_pending_records)
        AND(v_status = ARRAY[-1] OR v.previous_studies_states_id = ANY(v_status))
        AND (v.program_id = v_program OR v_program = -1)
        AND (im.acronym ILIKE '%' || filter || '%' OR v.code ILIKE '%' || filter || '%' OR filter = '')
        ORDER BY
            pending_my_approval desc,
            v.id DESC
        LIMIT 20 OFFSET (page - 1) * 20;

        RAISE NOTICE 'v_id_user: %', v_id_user;
        RAISE NOTICE 'v_program: %', v_program;
        RAISE NOTICE 'v_status: %', v_status;
        RAISE NOTICE 'filter: %', filter;
    END IF;

    drop table tmp_rol;
    drop table tmp_control;
    drop table tmp_pending_records;
END;
$BODY$;
    """)
 


def downgrade() -> None:
    op.execute("""
        DROP FUNCTION IF EXISTS public.list_previous_studies;
        """)
