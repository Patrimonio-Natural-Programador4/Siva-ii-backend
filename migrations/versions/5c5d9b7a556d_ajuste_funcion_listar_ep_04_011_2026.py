"""Ajuste_funcion_listar_EP_04_011_2026

Revision ID: 5c5d9b7a556d
Revises: b126ef012954
Create Date: 2026-11-04 10:01:09.934705

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c5d9b7a556d'
down_revision: Union[str, Sequence[str], None] = 'b126ef012954'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
     op.execute("""
              DROP FUNCTION IF EXISTS public.list_previous_studies(
             CHARACTER VARYING, INTEGER, INTEGER[], CHARACTER VARYING, INTEGER[]
                );
           """)
     
     op.execute("""
                   CREATE OR REPLACE FUNCTION public.list_previous_studies(guid_user_msft character varying, page integer DEFAULT 1, v_status integer[] DEFAULT ARRAY['-1'::integer], filter character varying DEFAULT ''::character varying, v_program integer[] DEFAULT ARRAY['-1'::integer])
 RETURNS TABLE(precedents text, justification text, scope text, overall_objective text, term text, obligations text, supervisor text, total_value bigint, contributions_ei bigint, total_value_executes_fpn bigint, total_value_executes_ei bigint, previous_studies_states_id integer, implementer_id bigint, implementer_name citext, persons_id bigint, persons_email character varying, capacity_assessment_id bigint, capacity_assessment_name text, guid uuid, program_id bigint, program_name citext, contributions_fpn bigint, estimated_term text, code text, previous_studies_states_name text, pending_my_approval boolean, approval_request_id bigint, user_id bigint, guid_msft uuid, step_order_actual_request integer, guid_msft_adjustment uuid, total_records bigint, previous_study_id bigint, code_agreements text, rol text, implementadora text, fecha_crea timestamp without time zone, fecha_aprobacion timestamp without time zone, pilar text, lider_pilar text, usuario text, tipo_convenio text, modalidad_id bigint, modalidad text, estado_aprobacion text, id_capacity_state_id bigint, capacity_state text)
 LANGUAGE plpgsql
AS $function$
DECLARE
    v_id_user                  INT;
    v_list_all_request         INT;
    v_list_supervised_requests INT;
    v_offset                   INT;
BEGIN
    
    -- Usuario y paginación
    
    SELECT u.id
      INTO v_id_user
      FROM users u
     WHERE u.guid_msft = guid_user_msft::UUID;

    v_offset := (page - 1) * 20;

    RAISE NOTICE 'TS: %', v_status;

    
    -- Roles del usuario
    
    CREATE TEMPORARY TABLE tmp_rol AS
    SELECT mhr.role_id
      FROM model_has_roles mhr
     WHERE mhr.model_id = v_id_user;

  
    -- Controles con validación del módulo ADM_STU_PREV
  
    CREATE TEMPORARY TABLE tmp_control AS
    SELECT ctl.code
      FROM control_access ca
     INNER JOIN controls ctl ON ca.control_id = ctl.control_id
     INNER JOIN modules  mo  ON ctl.module_id = mo.id
     WHERE ca.role_id IN (SELECT role_id FROM tmp_rol)
       AND ctl.requires_validation = TRUE
       AND mo.code = 'ADM_STU_PREV';

  
    -- Registros pendientes de aprobación del usuario
  

    -- Asignados directamente al usuario
    CREATE TEMPORARY TABLE tmp_pending_records AS
    SELECT ar.related_record_id
      FROM approval_request_history arh
     INNER JOIN approval_requests   ar  ON arh.approval_request_id = ar.approval_request_id
     INNER JOIN approval_flows      af  ON ar.approval_workflow_id = af.approval_flow_id
     INNER JOIN approval_categories cat ON af.category_id          = cat.category_id
     WHERE arh.approval_status_id = 6
       AND arh.user_id            = v_id_user
       AND cat.code               = 'APP_EP';

    -- Asignados al rol del usuario (sin usuario específico)
    INSERT INTO tmp_pending_records
    SELECT ar.related_record_id
      FROM approval_request_history arh
     INNER JOIN approval_requests   ar  ON arh.approval_request_id = ar.approval_request_id
     INNER JOIN approval_flows      af  ON ar.approval_workflow_id = af.approval_flow_id
     INNER JOIN approval_role_users aru ON arh.approval_role_id    = aru.approval_role_id
     INNER JOIN approval_categories cat ON af.category_id          = cat.category_id
     WHERE arh.approval_status_id = 6
       AND ar.approval_status_id  = 6
       AND aru.user_id            = v_id_user
       AND arh.user_id IS NULL
       AND cat.code               = 'APP_EP';

  
    -- Permisos: TS = ver todas | UBS = supervisadas
  
    
    SELECT COUNT(*) INTO v_list_all_request
      FROM tmp_control tc
     WHERE tc.code = 'TS';

    SELECT COUNT(*) INTO v_list_supervised_requests
      FROM tmp_control tc
     WHERE tc.code = 'UBS';

  
  
  
    IF v_list_all_request > 0 THEN
        
        --Usuario con permiso TS: ve todos los estudios
        
        RAISE NOTICE 'Entro: %', v_list_all_request;

        RETURN QUERY
        SELECT
            v.precedents,
            v.justification,
            v.scope,
            v.overall_objective,
            v.term,
            v.obligations,
            v.supervisor,
            v.total_value,
            v.contributions_ei,
            v.total_value_executes_fpn,
            v.total_value_executes_ei,
            v.previous_studies_states_id,
            v.implementer_id,
            im.acronym                AS implementer_name,
            v.persons_id,
            p.email                   AS persons_email,
            v.capacity_assessment_id,
            ca.name                   AS capacity_assessment_name,
            v.guid,
            v.program_id,
            pr.name                   AS program_name,
            v.contributions_fpn,
            v.estimated_term,
            v.code,
            st.state                  AS previous_studies_states_name,
            CASE
                WHEN (v.id IN (SELECT related_record_id FROM tmp_pending_records)
                      AND v.previous_studies_states_id IN (2))
                  OR (v.previous_studies_states_id = 3
                      AND v.user_session = v_id_user)
                THEN TRUE
                ELSE FALSE
            END                       AS pending_my_approval,
            v.approval_request_id,
            v.user_session            AS user_id,
            u.guid_msft,
            CASE WHEN v.approval_request_id IS NULL THEN 0    ELSE sv.step_order           END AS step_order_actual_request,
            CASE WHEN v.approval_request_id IS NULL THEN NULL ELSE sv.guid_msft_adjustment END AS guid_msft_adjustment,
            COUNT(*) OVER ()          AS total_records,
           
            v.id::BIGINT                                      AS previous_study_id,
            ar.code::TEXT                                     AS code_agreements,
            vh.rol::TEXT                                      AS rol,
            im.name::TEXT                                     AS implementadora,
            vh.created_at::TIMESTAMP                          AS fecha_crea,
            vh.approved_at::TIMESTAMP                         AS fecha_aprobacion,
            pi.name::TEXT                                     AS pilar,
            concat_ws(' ', pe.first_name, pe.last_name)::TEXT AS lider_pilar,
            COALESCE(vh."user", resp.responsables)::TEXT      AS usuario,
            atp.name::TEXT                                    AS tipo_convenio,
            mdl.id::BIGINT                                    AS modalidad_id,
            mdl.name::TEXT                                    AS modalidad,
            vh.approval_route_status::TEXT                    AS estado_aprobacion,
            caes.id::BIGINT                                   AS id_capacity_state_id,
            caes.state::TEXT                                  AS capacity_state
        FROM previous_studies v
        INNER JOIN users                       u    ON v.user_session               = u.id
        INNER JOIN previous_studies_states     st   ON v.previous_studies_states_id = st.id
        LEFT  JOIN implementers                im   ON v.implementer_id             = im.id
        LEFT  JOIN programs                    pr   ON v.program_id                 = pr.id
        LEFT  JOIN persons                     p    ON v.persons_id                 = p.id
        LEFT  JOIN capacity_assessments        ca   ON v.capacity_assessment_id     = ca.id
       
        LEFT  JOIN approval_requests           ar   ON ar.approval_request_id       = v.approval_request_id
        LEFT  JOIN capacity_assessments_states caes ON caes.id                      = ca.capacity_assessments_states_id
        LEFT  JOIN pillars                     pi   ON pi.id                        = ca.pillar_id
        LEFT  JOIN persons                     pe   ON pe.id                        = pi.person_id
        LEFT  JOIN agreement_types             atp  ON atp.id                       = v.agreement_type_id
        LEFT  JOIN modalities                  mdl  ON mdl.id                       = v.modality_id
        LEFT  JOIN LATERAL (
            
            SELECT
                '(' || ra.name
                    || CASE WHEN us.full_name IS NULL THEN '' ELSE ' -> ' || us.full_name END
                    || ')'        AS responsable,
                fs.step_order,
                us.guid_msft      AS guid_msft_adjustment
            FROM approval_request_history hi
            INNER JOIN approval_roles      ra ON hi.approval_role_id = ra.approval_role_id
            LEFT  JOIN users               us ON hi.user_id          = us.id
            LEFT  JOIN approval_flow_steps fs ON hi.step_id          = fs.step_id
            WHERE hi.approval_request_id = v.approval_request_id
            ORDER BY hi.history_id DESC
            LIMIT 1
        ) sv ON TRUE
        LEFT  JOIN LATERAL (
           
            SELECT h.rol, h.created_at, h.approved_at, h."user",
                   h.approval_route_status, h.approval_role_id
            FROM vw_approval_request_history h
            WHERE h.approval_request_id = v.approval_request_id
            ORDER BY h.history_id DESC
            LIMIT 1
        ) vh ON TRUE
        LEFT  JOIN LATERAL (
           
            SELECT string_agg(
                       UPPER(concat_ws(' ', ru.first_name, NULLIF(ru.other_name, ''), ru.last_name)),
                       ', ' ORDER BY ru.first_name, ru.last_name
                   ) AS responsables
            FROM approval_role_users aru
            JOIN users ru ON ru.id = aru.user_id
            WHERE aru.approval_role_id = vh.approval_role_id
        ) resp ON TRUE
        WHERE (v_status = ARRAY[-1] OR v.previous_studies_states_id = ANY (v_status))
          AND (-1 = ANY (v_program) OR v.program_id = ANY (v_program))
          AND (filter = ''
               OR im.acronym ILIKE '%' || filter || '%'
               OR v.code     ILIKE '%' || filter || '%')
        ORDER BY pending_my_approval DESC, v.id DESC
        LIMIT 20 OFFSET v_offset;

    ELSE
        
        -- Usuario sin TS: solo los suyos o pendientes de él
        
        RAISE NOTICE 'ENTRO 2: %', v_list_all_request;

        RETURN QUERY
        SELECT
            v.precedents,
            v.justification,
            v.scope,
            v.overall_objective,
            v.term,
            v.obligations,
            v.supervisor,
            v.total_value,
            v.contributions_ei,
            v.total_value_executes_fpn,
            v.total_value_executes_ei,
            v.previous_studies_states_id,
            v.implementer_id,
            im.acronym                AS implementer_name,
            v.persons_id,
            p.email                   AS persons_email,
            v.capacity_assessment_id,
            ca.name                   AS capacity_assessment_name,
            v.guid,
            v.program_id,
            pr.name                   AS program_name,
            v.contributions_fpn,
            v.estimated_term,
            v.code,
            st.state                  AS previous_studies_states_name,
            CASE
                WHEN (v.id IN (SELECT related_record_id FROM tmp_pending_records)
                      AND v.previous_studies_states_id IN (2))
                  OR (v.previous_studies_states_id = 3
                      AND v.user_session = v_id_user)
                THEN TRUE
                ELSE FALSE
            END                       AS pending_my_approval,
            v.approval_request_id,
            v.user_session            AS user_id,
            u.guid_msft,
            CASE WHEN v.approval_request_id IS NULL THEN 0    ELSE sv.step_order           END AS step_order_actual_request,
            CASE WHEN v.approval_request_id IS NULL THEN NULL ELSE sv.guid_msft_adjustment END AS guid_msft_adjustment,
            COUNT(*) OVER ()          AS total_records,
            
            v.id::BIGINT                                      AS previous_study_id,
            ar.code::TEXT                                     AS code_agreements,
            vh.rol::TEXT                                      AS rol,
            im.name::TEXT                                     AS implementadora,
            vh.created_at::TIMESTAMP                          AS fecha_crea,
            vh.approved_at::TIMESTAMP                         AS fecha_aprobacion,
            pi.name::TEXT                                     AS pilar,
            concat_ws(' ', pe.first_name, pe.last_name)::TEXT AS lider_pilar,
            COALESCE(vh."user", resp.responsables)::TEXT      AS usuario,
            atp.name::TEXT                                    AS tipo_convenio,
            mdl.id::BIGINT                                    AS modalidad_id,
            mdl.name::TEXT                                    AS modalidad,
            vh.approval_route_status::TEXT                    AS estado_aprobacion,
            caes.id::BIGINT                                   AS id_capacity_state_id,
            caes.state::TEXT                                  AS capacity_state
        FROM previous_studies v
        INNER JOIN users                       u    ON v.user_session               = u.id
        INNER JOIN previous_studies_states     st   ON v.previous_studies_states_id = st.id
        LEFT  JOIN implementers                im   ON v.implementer_id             = im.id
        LEFT  JOIN programs                    pr   ON v.program_id                 = pr.id
        LEFT  JOIN persons                     p    ON v.persons_id                 = p.id
        LEFT  JOIN capacity_assessments        ca   ON v.capacity_assessment_id     = ca.id
    
        LEFT  JOIN approval_requests           ar   ON ar.approval_request_id       = v.approval_request_id
        LEFT  JOIN capacity_assessments_states caes ON caes.id                      = ca.capacity_assessments_states_id
        LEFT  JOIN pillars                     pi   ON pi.id                        = ca.pillar_id
        LEFT  JOIN persons                     pe   ON pe.id                        = pi.person_id
        LEFT  JOIN agreement_types             atp  ON atp.id                       = v.agreement_type_id
        LEFT  JOIN modalities                  mdl  ON mdl.id                       = v.modality_id
        LEFT  JOIN LATERAL (
       
            SELECT
                '(' || ra.name
                    || CASE WHEN us.full_name IS NULL THEN '' ELSE ' -> ' || us.full_name END
                    || ')'        AS responsable,
                fs.step_order,
                us.guid_msft      AS guid_msft_adjustment
            FROM approval_request_history hi
            INNER JOIN approval_roles      ra ON hi.approval_role_id = ra.approval_role_id
            LEFT  JOIN users               us ON hi.user_id          = us.id
            LEFT  JOIN approval_flow_steps fs ON hi.step_id          = fs.step_id
            WHERE hi.approval_request_id = v.approval_request_id
            ORDER BY hi.history_id DESC
            LIMIT 1
        ) sv ON TRUE
        LEFT  JOIN LATERAL (
           
            SELECT h.rol, h.created_at, h.approved_at, h."user",
                   h.approval_route_status, h.approval_role_id
            FROM vw_approval_request_history h
            WHERE h.approval_request_id = v.approval_request_id
            ORDER BY h.history_id DESC
            LIMIT 1
        ) vh ON TRUE
        LEFT  JOIN LATERAL (
           
            SELECT string_agg(
                       UPPER(concat_ws(' ', ru.first_name, NULLIF(ru.other_name, ''), ru.last_name)),
                       ', ' ORDER BY ru.first_name, ru.last_name
                   ) AS responsables
            FROM approval_role_users aru
            JOIN users ru ON ru.id = aru.user_id
            WHERE aru.approval_role_id = vh.approval_role_id
        ) resp ON TRUE
        
        WHERE (    v.user_session = v_id_user
                OR v.id IN (SELECT related_record_id FROM tmp_pending_records))
          AND (v_status = ARRAY[-1] OR v.previous_studies_states_id = ANY (v_status))
          AND (-1 = ANY (v_program) OR v.program_id = ANY (v_program))
          AND (filter = ''
               OR im.acronym ILIKE '%' || filter || '%'
               OR v.code     ILIKE '%' || filter || '%')
        ORDER BY pending_my_approval DESC, v.id DESC
        LIMIT 20 OFFSET v_offset;

        RAISE NOTICE 'v_id_user: %', v_id_user;
        RAISE NOTICE 'v_program: %', v_program;
        RAISE NOTICE 'v_status: %',  v_status;
        RAISE NOTICE 'filter: %',    filter;
    END IF;

  
  
  
    DROP TABLE tmp_rol;
    DROP TABLE tmp_control;
    DROP TABLE tmp_pending_records;
END;
$function$

                """)
     
     


def downgrade() -> None:
   
   op.execute("""
              CREATE OR REPLACE FUNCTION public.list_previous_studies(
    guid_user_msft  CHARACTER VARYING,
    page            INTEGER           DEFAULT 1,
    v_status        INTEGER[]         DEFAULT ARRAY[-1],
    filter          CHARACTER VARYING DEFAULT '',
    v_program       INTEGER           DEFAULT -1
)
RETURNS TABLE (
    precedents                    TEXT,
    justification                 TEXT,
    scope                         TEXT,
    overall_objective             TEXT,
    term                          TEXT,
    obligations                   TEXT,
    supervisor                    TEXT,
    total_value                   BIGINT,
    contributions_ei              BIGINT,
    total_value_executes_fpn      BIGINT,
    total_value_executes_ei       BIGINT,
    previous_studies_states_id    INTEGER,
    implementer_id                BIGINT,
    implementer_name              CITEXT,
    persons_id                    BIGINT,
    persons_email                 CHARACTER VARYING,
    capacity_assessment_id        BIGINT,
    capacity_assessment_name      TEXT,
    guid                          UUID,
    program_id                    BIGINT,
    program_name                  CITEXT,
    contributions_fpn             BIGINT,
    estimated_term                TEXT,
    code                          TEXT,
    previous_studies_states_name  TEXT,
    pending_my_approval           BOOLEAN,
    approval_request_id           BIGINT,
    user_id                       BIGINT,
    guid_msft                     UUID,
    step_order_actual_request     INTEGER,
    guid_msft_adjustment          UUID,
    total_records                 BIGINT
)
LANGUAGE plpgsql
AS $function$
DECLARE
    v_id_user                  INT;
    v_list_all_request         INT;
    v_list_supervised_requests INT;
    v_offset                   INT;
BEGIN
    
    -- Usuario y paginación
    
    SELECT u.id
      INTO v_id_user
      FROM users u
     WHERE u.guid_msft = guid_user_msft::UUID;

    v_offset := (page - 1) * 20;

    RAISE NOTICE 'TS: %', v_status;

    
    -- Roles del usuario
    
    CREATE TEMPORARY TABLE tmp_rol AS
    SELECT mhr.role_id
      FROM model_has_roles mhr
     WHERE mhr.model_id = v_id_user;

    
    --  Controles con validación del módulo ADM_STU_PREV
    
    CREATE TEMPORARY TABLE tmp_control AS
    SELECT ctl.code
      FROM control_access ca
     INNER JOIN controls ctl ON ca.control_id = ctl.control_id
     INNER JOIN modules  mo  ON ctl.module_id = mo.id
     WHERE ca.role_id IN (SELECT role_id FROM tmp_rol)
       AND ctl.requires_validation = TRUE
       AND mo.code = 'ADM_STU_PREV';

    
    --  Registros pendientes de aprobación del usuario
       
    CREATE TEMPORARY TABLE tmp_pending_records AS
    SELECT ar.related_record_id
      FROM approval_request_history arh
     INNER JOIN approval_requests   ar  ON arh.approval_request_id = ar.approval_request_id
     INNER JOIN approval_flows      af  ON ar.approval_workflow_id = af.approval_flow_id
     INNER JOIN approval_categories cat ON af.category_id          = cat.category_id
     WHERE arh.approval_status_id = 6
       AND arh.user_id            = v_id_user
       AND cat.code               = 'APP_EP';

    
    INSERT INTO tmp_pending_records
    SELECT ar.related_record_id
      FROM approval_request_history arh
     INNER JOIN approval_requests   ar  ON arh.approval_request_id = ar.approval_request_id
     INNER JOIN approval_flows      af  ON ar.approval_workflow_id = af.approval_flow_id
     INNER JOIN approval_role_users aru ON arh.approval_role_id    = aru.approval_role_id
     INNER JOIN approval_categories cat ON af.category_id          = cat.category_id
     WHERE arh.approval_status_id = 6
       AND ar.approval_status_id  = 6
       AND aru.user_id            = v_id_user
       AND arh.user_id IS NULL
       AND cat.code               = 'APP_EP';

   
    -- Permisos: TS = ver todas | UBS = supervisadas
  
    SELECT COUNT(*) INTO v_list_all_request
      FROM tmp_control
     WHERE code = 'TS';

    SELECT COUNT(*) INTO v_list_supervised_requests
      FROM tmp_control
     WHERE code = 'UBS';

   
    IF v_list_all_request > 0 THEN
       
        -- Usuario con permiso TS: ve todos los estudios
       
        RAISE NOTICE 'Entro: %', v_list_all_request;

        RETURN QUERY
        SELECT
            v.precedents,
            v.justification,
            v.scope,
            v.overall_objective,
            v.term,
            v.obligations,
            v.supervisor,
            v.total_value,
            v.contributions_ei,
            v.total_value_executes_fpn,
            v.total_value_executes_ei,
            v.previous_studies_states_id,
            v.implementer_id,
            im.acronym                AS implementer_name,
            v.persons_id,
            p.email                   AS persons_email,
            v.capacity_assessment_id,
            ca.name                   AS capacity_assessment_name,
            v.guid,
            v.program_id,
            pr.name                   AS program_name,
            v.contributions_fpn,
            v.estimated_term,
            v.code,
            st.state                  AS previous_studies_states_name,
            CASE
                WHEN (v.id IN (SELECT related_record_id FROM tmp_pending_records)
                      AND v.previous_studies_states_id IN (2))
                  OR (v.previous_studies_states_id = 3
                      AND v.user_session = v_id_user)
                THEN TRUE
                ELSE FALSE
            END                       AS pending_my_approval,
            v.approval_request_id,
            v.user_session            AS user_id,
            u.guid_msft,
            CASE WHEN v.approval_request_id IS NULL THEN 0    ELSE sv.step_order           END AS step_order_actual_request,
            CASE WHEN v.approval_request_id IS NULL THEN NULL ELSE sv.guid_msft_adjustment END AS guid_msft_adjustment,
            COUNT(*) OVER ()          AS total_records
        FROM previous_studies v
        INNER JOIN users                   u  ON v.user_session               = u.id
        INNER JOIN previous_studies_states st ON v.previous_studies_states_id = st.id
        LEFT  JOIN implementers            im ON v.implementer_id             = im.id
        LEFT  JOIN programs                pr ON v.program_id                 = pr.id
        LEFT  JOIN persons                 p  ON v.persons_id                 = p.id
        LEFT  JOIN capacity_assessments    ca ON v.capacity_assessment_id     = ca.id
        LEFT  JOIN LATERAL (
            -- Último paso del historial de aprobación
            SELECT
                '(' || ra.name
                    || CASE WHEN us.full_name IS NULL THEN '' ELSE ' -> ' || us.full_name END
                    || ')'        AS responsable,
                fs.step_order,
                us.guid_msft      AS guid_msft_adjustment
            FROM approval_request_history hi
            INNER JOIN approval_roles      ra ON hi.approval_role_id = ra.approval_role_id
            LEFT  JOIN users               us ON hi.user_id          = us.id
            LEFT  JOIN approval_flow_steps fs ON hi.step_id          = fs.step_id
            WHERE hi.approval_request_id = v.approval_request_id
            ORDER BY hi.history_id DESC
            LIMIT 1
        ) sv ON TRUE
        WHERE (v_status = ARRAY[-1] OR v.previous_studies_states_id = ANY (v_status))
          AND (v_program = -1 OR v.program_id = v_program)
          AND (filter = ''
               OR im.acronym ILIKE '%' || filter || '%'
               OR v.code     ILIKE '%' || filter || '%')
        ORDER BY pending_my_approval DESC, v.id DESC
        LIMIT 20 OFFSET v_offset;

    ELSE
       
        --  Usuario sin TS: solo los suyos o pendientes de él
        
        RAISE NOTICE 'ENTRO 2: %', v_list_all_request;

        RETURN QUERY
        SELECT
            v.precedents,
            v.justification,
            v.scope,
            v.overall_objective,
            v.term,
            v.obligations,
            v.supervisor,
            v.total_value,
            v.contributions_ei,
            v.total_value_executes_fpn,
            v.total_value_executes_ei,
            v.previous_studies_states_id,
            v.implementer_id,
            im.acronym                AS implementer_name,
            v.persons_id,
            p.email                   AS persons_email,
            v.capacity_assessment_id,
            ca.name                   AS capacity_assessment_name,
            v.guid,
            v.program_id,
            pr.name                   AS program_name,
            v.contributions_fpn,
            v.estimated_term,
            v.code,
            st.state                  AS previous_studies_states_name,
            CASE
                WHEN (v.id IN (SELECT related_record_id FROM tmp_pending_records)
                      AND v.previous_studies_states_id IN (2))
                  OR (v.previous_studies_states_id = 3
                      AND v.user_session = v_id_user)
                THEN TRUE
                ELSE FALSE
            END                       AS pending_my_approval,
            v.approval_request_id,
            v.user_session            AS user_id,
            u.guid_msft,
            CASE WHEN v.approval_request_id IS NULL THEN 0    ELSE sv.step_order           END AS step_order_actual_request,
            CASE WHEN v.approval_request_id IS NULL THEN NULL ELSE sv.guid_msft_adjustment END AS guid_msft_adjustment,
            COUNT(*) OVER ()          AS total_records
        FROM previous_studies v
        INNER JOIN users                   u  ON v.user_session               = u.id
        INNER JOIN previous_studies_states st ON v.previous_studies_states_id = st.id
        LEFT  JOIN implementers            im ON v.implementer_id             = im.id
        LEFT  JOIN programs                pr ON v.program_id                 = pr.id
        LEFT  JOIN persons                 p  ON v.persons_id                 = p.id
        LEFT  JOIN capacity_assessments    ca ON v.capacity_assessment_id     = ca.id
        LEFT  JOIN LATERAL (
            -- Último paso del historial de aprobación
            SELECT
                '(' || ra.name
                    || CASE WHEN us.full_name IS NULL THEN '' ELSE ' -> ' || us.full_name END
                    || ')'        AS responsable,
                fs.step_order,
                us.guid_msft      AS guid_msft_adjustment
            FROM approval_request_history hi
            INNER JOIN approval_roles      ra ON hi.approval_role_id = ra.approval_role_id
            LEFT  JOIN users               us ON hi.user_id          = us.id
            LEFT  JOIN approval_flow_steps fs ON hi.step_id          = fs.step_id
            WHERE hi.approval_request_id = v.approval_request_id
            ORDER BY hi.history_id DESC
            LIMIT 1
        ) sv ON TRUE
        -- ⚠ Paréntesis explícitos = mismo comportamiento que la versión original (ver nota 1)
        WHERE v.user_session = v_id_user
           OR (    v.id IN (SELECT related_record_id FROM tmp_pending_records)
               AND (v_status = ARRAY[-1] OR v.previous_studies_states_id = ANY (v_status))
               AND (v_program = -1 OR v.program_id = v_program)
               AND (filter = ''
                    OR im.acronym ILIKE '%' || filter || '%'
                    OR v.code     ILIKE '%' || filter || '%'))
        ORDER BY pending_my_approval DESC, v.id DESC
        LIMIT 20 OFFSET v_offset;

        RAISE NOTICE 'v_id_user: %', v_id_user;
        RAISE NOTICE 'v_program: %', v_program;
        RAISE NOTICE 'v_status: %',  v_status;
        RAISE NOTICE 'filter: %',    filter;
    END IF;

 
    DROP TABLE tmp_rol;
    DROP TABLE tmp_control;
    DROP TABLE tmp_pending_records;
END;
$function$;
           """)