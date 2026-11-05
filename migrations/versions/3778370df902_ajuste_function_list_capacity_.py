"""ajuste_function_list_capacity_assesstment_05_11_2026

Revision ID: 3778370df902
Revises: 7dcdd838aa64
Create Date: 2026-11-05 16:08:40.511193

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3778370df902'
down_revision: Union[str, Sequence[str], None] = '7dcdd838aa64'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        '''
        DROP FUNCTION IF EXISTS public.list_capacity_assesstment(
            CHARACTER VARYING,
            INTEGER,
            INTEGER[],
            CHARACTER VARYING,
            INTEGER
);
                
        '''
        
    )

    op.execute(
        ''' 
        

CREATE OR REPLACE FUNCTION public.list_capacity_assesstment(
    guid_user_msft CHARACTER VARYING,
    page           INTEGER           DEFAULT 1,
    v_status       INTEGER[]         DEFAULT ARRAY['-1'::INTEGER],
    filter         CHARACTER VARYING DEFAULT ''::CHARACTER VARYING,
    v_program      INTEGER           DEFAULT '-1'::INTEGER
)
RETURNS TABLE (
    guid                           UUID,
    name                           TEXT,
    observation                    TEXT,
    approximate_value              BIGINT,
    implementer_id                 BIGINT,
    implementer_name               CITEXT,
    policy_approval_date           DATE,
    document_signature_date        DATE,
    start_date                     DATE,
    end_date                       DATE,
    code                           TEXT,
    program_id                     BIGINT,
    program_name                   CITEXT,
    pid_id                         BIGINT,
    pad_name                       CHARACTER VARYING,
    persons_id                     BIGINT,
    persons_email                  CHARACTER VARYING,
    capacity_assessments_states_id BIGINT,
    modality_id                    BIGINT,
    modality_name                  CHARACTER VARYING,
    pending_my_approval            BOOLEAN,
    capacity_assestments_id        INTEGER,
    approval_request_id            BIGINT,
    user_id                        BIGINT,
    guid_msft                      UUID,
    step_order_actual_request      INTEGER,
    guid_msft_adjustment           UUID,
    total_records                  BIGINT,
    is_deleted                     BOOLEAN
)
LANGUAGE plpgsql
AS $function$
DECLARE
    v_id_user                 INT;
    v_list_all_request        INT;
    v_list_supervised_requests INT;
    v_offset                  INT;
BEGIN

    SELECT u.id
      INTO v_id_user
      FROM users u
     WHERE u.guid_msft = guid_user_msft::UUID;

    RAISE NOTICE 'TS: %', v_status;

    v_offset := (page - 1) * 20;

    CREATE TEMPORARY TABLE tmp_rol AS
    SELECT mhr.role_id
      FROM model_has_roles mhr
     WHERE mhr.model_id = v_id_user;

    CREATE TEMPORARY TABLE tmp_control AS
    SELECT ctl.code
      FROM control_access ca
     INNER JOIN controls ctl ON ca.control_id = ctl.control_id
     INNER JOIN modules  mo  ON ctl.module_id = mo.id
     WHERE ca.role_id IN (SELECT role_id FROM tmp_rol)
       AND ctl.requires_validation = TRUE
       AND mo.code = 'ADM_CAP_ASSE';

    CREATE TEMPORARY TABLE tmp_pending_records AS
    SELECT ar.related_record_id
      FROM approval_request_history arh
     INNER JOIN approval_requests   ar  ON arh.approval_request_id = ar.approval_request_id
     INNER JOIN approval_flows      af  ON ar.approval_workflow_id = af.approval_flow_id
     INNER JOIN approval_categories cat ON af.category_id          = cat.category_id
     WHERE arh.approval_status_id = 6
       AND arh.user_id = v_id_user
       AND cat.code = 'APP_EC';

    INSERT INTO tmp_pending_records
    SELECT ar.related_record_id
      FROM approval_request_history arh
     INNER JOIN approval_requests   ar  ON arh.approval_request_id = ar.approval_request_id
     INNER JOIN approval_flows      af  ON ar.approval_workflow_id = af.approval_flow_id
     INNER JOIN approval_role_users aru ON arh.approval_role_id    = aru.approval_role_id
     INNER JOIN approval_categories cat ON af.category_id          = cat.category_id
     WHERE arh.approval_status_id = 6
       AND ar.approval_status_id = 6
       AND aru.user_id = v_id_user
       AND arh.user_id IS NULL
       AND cat.code = 'APP_EC';

    SELECT COUNT(*)
      INTO v_list_all_request
      FROM tmp_control tc
     WHERE tc.code = 'TS';

    SELECT COUNT(*)
      INTO v_list_supervised_requests
      FROM tmp_control tc
     WHERE tc.code = 'UBS';

    IF v_list_all_request > 0 THEN

        RAISE NOTICE 'Entro: %', v_list_all_request;

        RETURN QUERY
        SELECT
            v.guid,
            v.name,
            v.observation,
            v.approximate_value,
            v.implementer_id,
            im.acronym,
            v.policy_approval_date,
            v.document_signature_date,
            v.start_date,
            v.end_date,
            v.code,
            v.program_id,
            c.name,
            v.pid_id,
            p.pad,
            v.persons_id,
            d.email,
            v.capacity_assessments_states_id,
            v.modality_id,
            m.name,
            CASE
                WHEN (v.id IN (SELECT related_record_id FROM tmp_pending_records)
                      AND v.capacity_assessments_states_id = 2)
                  OR (v.capacity_assessments_states_id = 3
                      AND v.user_session = v_id_user)
                THEN TRUE
                ELSE FALSE
            END AS pending_my_approval,
            v.id,
            v.approval_request_id,
            v.user_session,
            a.guid_msft,
            CASE WHEN v.approval_request_id IS NULL THEN 0    ELSE sv.step_order           END AS step_order_actual_request,
            CASE WHEN v.approval_request_id IS NULL THEN NULL ELSE sv.guid_msft_adjustment END AS guid_msft_adjustment,
            COUNT(*) OVER () AS total_records,
            v.is_deleted

          FROM capacity_assessments v
         INNER JOIN users                      a  ON v.user_session                   = a.id
         INNER JOIN capacity_assessments_states b ON v.capacity_assessments_states_id = b.id
          LEFT JOIN implementers               im ON v.implementer_id                 = im.id
          LEFT JOIN programs                   c  ON v.program_id                     = c.id
          LEFT JOIN pids                       p  ON v.pid_id                         = p.id
          LEFT JOIN modalities                 m  ON v.modality_id                    = m.id
          LEFT JOIN persons                    d  ON v.persons_id                     = d.id
          LEFT JOIN LATERAL (
                SELECT
                    '(' || ra.name ||
                    CASE WHEN us.full_name IS NULL THEN '' ELSE ' -> ' || us.full_name END ||
                    ')' AS responsable,
                    fr.step_order,
                    us.guid_msft AS guid_msft_adjustment
                  FROM approval_request_history hi
                 INNER JOIN approval_roles      ra ON hi.approval_role_id = ra.approval_role_id
                  LEFT JOIN users               us ON hi.user_id          = us.id
                  LEFT JOIN approval_flow_steps fr ON hi.step_id          = fr.step_id
                 WHERE hi.approval_request_id = v.approval_request_id
                 ORDER BY hi.history_id DESC
                 LIMIT 1
          ) sv ON TRUE
         WHERE (v_status = ARRAY[-1] OR v.capacity_assessments_states_id = ANY (v_status))
           AND (v_program = -1 OR v.program_id = v_program)
           AND (filter = '' OR im.acronym ILIKE '%' || filter || '%' OR v.code ILIKE '%' || filter || '%')
         ORDER BY
            pending_my_approval DESC,
            v.id DESC
         LIMIT 20 OFFSET v_offset;

    ELSE

        RAISE NOTICE 'ENTRO 2: %', v_list_all_request;

        RETURN QUERY
        SELECT
            v.guid,
            v.name,
            v.observation,
            v.approximate_value,
            v.implementer_id,
            im.acronym,
            v.policy_approval_date,
            v.document_signature_date,
            v.start_date,
            v.end_date,
            v.code,
            v.program_id,
            c.name,
            v.pid_id,
            p.pad,
            v.persons_id,
            d.email,
            v.capacity_assessments_states_id,
            v.modality_id,
            m.name,
            CASE
                WHEN (v.id IN (SELECT related_record_id FROM tmp_pending_records)
                      AND v.capacity_assessments_states_id = 2)
                  OR (v.capacity_assessments_states_id = 3
                      AND v.user_session = v_id_user)
                THEN TRUE
                ELSE FALSE
            END AS pending_my_approval,
            v.id,
            v.approval_request_id,
            v.user_session,
            a.guid_msft,
            CASE WHEN v.approval_request_id IS NULL THEN 0    ELSE sv.step_order           END AS step_order_actual_request,
            CASE WHEN v.approval_request_id IS NULL THEN NULL ELSE sv.guid_msft_adjustment END AS guid_msft_adjustment,
            COUNT(*) OVER () AS total_records,
            v.is_deleted

          FROM capacity_assessments v
         INNER JOIN users                      a  ON v.user_session                   = a.id
         INNER JOIN capacity_assessments_states b ON v.capacity_assessments_states_id = b.id
          LEFT JOIN implementers               im ON v.implementer_id                 = im.id
          LEFT JOIN programs                   c  ON v.program_id                     = c.id
          LEFT JOIN pids                       p  ON v.pid_id                         = p.id
          LEFT JOIN modalities                 m  ON v.modality_id                    = m.id
          LEFT JOIN persons                    d  ON v.persons_id                     = d.id
          LEFT JOIN LATERAL (
                SELECT
                    '(' || ra.name ||
                    CASE WHEN us.full_name IS NULL THEN '' ELSE ' -> ' || us.full_name END ||
                    ')' AS responsable,
                    fr.step_order,
                    us.guid_msft AS guid_msft_adjustment
                  FROM approval_request_history hi
                 INNER JOIN approval_roles      ra ON hi.approval_role_id = ra.approval_role_id
                  LEFT JOIN users               us ON hi.user_id          = us.id
                  LEFT JOIN approval_flow_steps fr ON hi.step_id          = fr.step_id
                 WHERE hi.approval_request_id = v.approval_request_id
                 ORDER BY hi.history_id DESC
                 LIMIT 1
          ) sv ON TRUE
         WHERE v.user_session = v_id_user
            OR (
                    v.id IN (SELECT related_record_id FROM tmp_pending_records)
                AND (v_status = ARRAY[-1] OR v.capacity_assessments_states_id = ANY (v_status))
                AND (v_program = -1 OR v.program_id = v_program)
                AND (filter = '' OR im.acronym ILIKE '%' || filter || '%' OR v.code ILIKE '%' || filter || '%')
            )
         ORDER BY
            pending_my_approval DESC,
            v.id DESC
         LIMIT 20 OFFSET v_offset;

        RAISE NOTICE 'v_id_user: %', v_id_user;
        RAISE NOTICE 'v_program: %', v_program;
        RAISE NOTICE 'v_status: %', v_status;
        RAISE NOTICE 'filter: %', filter;

    END IF;

    DROP TABLE tmp_rol;
    DROP TABLE tmp_control;
    DROP TABLE tmp_pending_records;

END;
$function$;
        
        ''')

def downgrade() -> None:
   op.execute(
       '''
    
CREATE OR REPLACE FUNCTION public.list_capacity_assesstment(guid_user_msft character varying, page integer DEFAULT 1, v_status integer[] DEFAULT ARRAY['-1'::integer], filter character varying DEFAULT ''::character varying, v_program integer DEFAULT '-1'::integer)
 RETURNS TABLE(guid uuid, name text, observation text, approximate_value bigint, implementer_id bigint, implementer_name citext, policy_approval_date date, document_signature_date date, start_date date, end_date date, code text, program_id bigint, program_name citext, pid_id bigint, pad_name character varying, persons_id bigint, persons_email character varying, capacity_assessments_states_id bigint, modality_id bigint, modality_name character varying, pending_my_approval boolean, capacity_assestments_id integer, approval_request_id bigint, user_id bigint, guid_msft uuid, step_order_actual_request integer, guid_msft_adjustment uuid, total_records bigint)
 LANGUAGE plpgsql
AS $function$
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
    AND c.code = 'ADM_CAP_ASSE';

    CREATE TEMPORARY TABLE tmp_pending_records AS
    SELECT b.related_record_id
    FROM approval_request_history a
    INNER JOIN approval_requests b ON a.approval_request_id = b.approval_request_id
    INNER JOIN approval_flows c ON b.approval_workflow_id = c.approval_flow_id
    INNER JOIN approval_categories e on c.category_id = e.category_id
    WHERE a.approval_status_id = 6
    AND a.user_id = v_id_user
    AND e.code = 'APP_EC';

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
    AND e.code = 'APP_EC';

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
            v.guid,
            v.name,
            v.observation,
            v.approximate_value,
            v.implementer_id,
            im.acronym,
            v.policy_approval_date,
            v.document_signature_date,
            v.start_date,
            v.end_date,
            v.code,
            v.program_id,
            c.name,
            v.pid_id,
            p.pad,
            v.persons_id,
            d.email,
            v.capacity_assessments_states_id,
            v.modality_id,
            m.name,
            CASE
                WHEN (v.id IN (SELECT related_record_id FROM tmp_pending_records) and v.capacity_assessments_states_id =2) or (v.capacity_assessments_states_id = 3 and v.user_session = v_id_user) THEN true
                ELSE false
            END AS pending_my_approval,
            v.id,
            v.approval_request_id,
            v.user_session,
            a.guid_msft,
            case when v.approval_request_id is null then 0 else sv.step_order  end  step_order_actual_request,
            case when v.approval_request_id is null then null else sv.guid_msft_adjustment end  guid_msft_adjustment,
            COUNT(*) OVER() AS total_records
        FROM capacity_assessments v
        INNER JOIN users a ON v.user_session = a.id
        INNER JOIN capacity_assessments_states b ON v.capacity_assessments_states_id = b.id
        LEFT JOIN implementers im on v.implementer_id = im.id
        LEFT JOIN programs c on v.program_id = c.id
        LEFT JOIN pids p on v.pid_id = p.id
        LEFT JOIN modalities m on v.modality_id = m.id
        LEFT JOIN persons d on v.persons_id = d.id
        LEFT JOIN LATERAL (
    SELECT
        '(' || RA.NAME || CASE
            WHEN US.FULL_NAME IS NULL THEN ''
            ELSE ' -> ' || US.FULL_NAME
        END || ')' AS RESPONSABLE,
        FR.STEP_ORDER,
        US.GUID_MSFT AS GUID_MSFT_ADJUSTMENT
    FROM
        APPROVAL_REQUEST_HISTORY HI
        INNER JOIN APPROVAL_ROLES RA ON HI.APPROVAL_ROLE_ID = RA.APPROVAL_ROLE_ID
        LEFT JOIN USERS US ON HI.USER_ID = US.ID
        LEFT JOIN APPROVAL_FLOW_STEPS FR ON HI.STEP_ID = FR.STEP_ID
    WHERE
        V.APPROVAL_REQUEST_ID = HI.APPROVAL_REQUEST_ID
    ORDER BY
        HI.HISTORY_ID DESC
    LIMIT
        1
) SV ON TRUE
       WHERE (v_status = ARRAY[-1] OR v.capacity_assessments_states_id = ANY(v_status))
        AND (v.program_id = v_program OR v_program = -1)
        AND (im.acronym ILIKE '%' || filter || '%' OR v.code ILIKE '%' || filter || '%' OR filter = '')
        ORDER BY
            pending_my_approval desc,
            v.id DESC
        LIMIT 20 OFFSET (page - 1) * 20;
    ELSE
    RAISE NOTICE 'ENTRO 2: %', v_list_all_request;
        RETURN QUERY
        SELECT
            v.guid,
            v.name,
            v.observation,
            v.approximate_value,
            v.implementer_id,
            im.acronym,
            v.policy_approval_date,
            v.document_signature_date,
            v.start_date,
            v.end_date,
            v.code,
            v.program_id,
            c.name,
            v.pid_id,
            p.pad,
            v.persons_id,
            d.email,
            v.capacity_assessments_states_id,
            v.modality_id,
            m.name,
            CASE
                WHEN (v.id IN (SELECT related_record_id FROM tmp_pending_records) and v.capacity_assessments_states_id = 2) or (v.capacity_assessments_states_id = 3 and v.user_session = v_id_user) THEN true
                ELSE false
            END AS pending_my_approval,
            v.id,
            v.approval_request_id,
            v.user_session,
            a.guid_msft,
            case when v.approval_request_id is null then 0 else sv.step_order  end  step_order_actual_request,
            case when v.approval_request_id is null then null else sv.guid_msft_adjustment end  guid_msft_adjustment,
            COUNT(*) OVER() AS total_records
        FROM capacity_assessments v
        INNER JOIN users a ON v.user_session = a.id
        INNER JOIN capacity_assessments_states b ON v.capacity_assessments_states_id = b.id
        LEFT JOIN implementers im on v.implementer_id = im.id
        LEFT JOIN programs c on v.program_id = c.id
        LEFT JOIN pids p on v.pid_id = p.id
        LEFT JOIN modalities m on v.modality_id = m.id
        LEFT JOIN persons d on v.persons_id = d.id
        LEFT JOIN LATERAL (
            SELECT '(' || ra.name || case when us.full_name is null then '' else  ' -> ' || us.full_name end ||')' as responsable, fr.step_order,
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
        AND(v_status = ARRAY[-1] OR v.capacity_assessments_states_id = ANY(v_status))
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
$function$
              
              
              
              '''
              )