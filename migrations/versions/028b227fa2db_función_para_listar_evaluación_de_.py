"""Función para listar evaluación de capacidades

Revision ID: 028b227fa2db
Revises: f67e554cd5d4
Create Date: 2026-08-21 16:35:32.856051

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '028b227fa2db'
down_revision: Union[str, Sequence[str], None] = 'f67e554cd5d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
    CREATE OR REPLACE FUNCTION public.list_capacity_assesstment(
	guid_user_msft character varying,
	page integer DEFAULT 1,
	v_status integer[] DEFAULT ARRAY['-1'::integer],
	filter character varying DEFAULT ''::character varying,
	--start_date date DEFAULT NULL::date,
	--end_date date DEFAULT NULL::date,
	v_program integer DEFAULT '-1'::integer)
    RETURNS TABLE(guid uuid, code text, name text, implementer_id bigint, implementer_name citext, pending_my_approval boolean,
    		capacity_assestments_id integer, approval_request_id bigint,  user_id bigint, guid_msft uuid,  step_order_actual_request integer, 
			guid_msft_adjustment uuid, total_records bigint) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
DECLARE
    v_id_user INT;
    v_list_all_request INT;
    v_list_supervised_requests INT;
    v_offset INT;
BEGIN

--select * from capacity_assessments
    -- Obtener el id_usuario usando el guid proporcionado
    -- Actualizado desde alembic
    SELECT a.id INTO v_id_user
    FROM users a
    WHERE a.guid_msft = guid_user_msft::UUID;

	RAISE NOTICE 'TS: %', v_status;

    -- Calcular el offset para la paginación
    v_offset = (page - 1) * 20;

    -- Crear tabla temporal para roles
    CREATE TEMPORARY TABLE tmp_rol AS
    SELECT a.role_id
    FROM model_has_roles a
    WHERE a.model_id = v_id_user;

    -- Crear tabla temporal para controles
    CREATE TEMPORARY TABLE tmp_control AS
    SELECT b.code
    FROM control_access a
    INNER JOIN controls b ON a.control_id = b.control_id
    INNER JOIN modules c ON b.module_id = c.id
    WHERE a.role_id IN (SELECT role_id FROM tmp_rol)
    AND b.requires_validation = TRUE
    AND c.code = 'ADM_CAP_ASSE';

    -- Crear tabla temporal para registros pendientes
    CREATE TEMPORARY TABLE tmp_pending_records AS
    SELECT b.related_record_id
    FROM approval_request_history a
    INNER JOIN approval_requests b ON a.approval_request_id = b.approval_request_id
    INNER JOIN approval_flows c ON b.approval_workflow_id = c.approval_flow_id
	INNER JOIN approval_categories e on c.category_id = e.category_id
    WHERE a.approval_status_id = 6
    AND a.user_id = v_id_user
    AND e.code = 'APP_EC';
	--2 = id_categoria aprobación viajes


    -- Insertar registros adicionales en la tabla de viajes pendientes
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

    -- Consultar el valor de "TS" y "UBS" en tmp_controles
    SELECT count(*) INTO v_list_all_request
    FROM tmp_control a
    WHERE a.code = 'TS';

    SELECT count(*) INTO v_list_supervised_requests
    FROM tmp_control a
    WHERE a.code = 'UBS';

    -- Lógica condicional
    IF v_list_all_request > 0 THEN

		RAISE NOTICE 'Entro: %', v_list_all_request;
        -- Si hay "TS", listar todos los viajes



		
        RETURN QUERY
        SELECT 
            v.guid, v.code, v.name, v.implementer_id, im.acronym,
            CASE 
                WHEN (v.id IN (SELECT related_record_id FROM tmp_pending_records) and v.capacity_assessments_states_id in (2,5)) or (v.capacity_assessments_states_id = 6 and v.user_session = v_id_user) THEN true
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
        /*AND (v.travel_end_date >= start_date OR start_date IS NULL)
        AND (v.travel_start_date <= end_date OR end_date IS NULL)*/
        ORDER BY 
            -- Primero los viajes que están en tmp_viajes_pendientes
            pending_my_approval desc,
            -- Luego ordenar por id_viaje descendente
            v.id DESC
        LIMIT 20 OFFSET (page - 1) * 20;
    ELSE
	RAISE NOTICE 'ENTRO 2: %', v_list_all_request;
        -- Si no hay "TS" ni "UBS", solo mostrar viajes relacionados con el usuario o viajes pendientes
        RETURN QUERY
        SELECT 
            v.guid, v.code, v.name, v.implementer_id, im.acronym,
            CASE 
                WHEN (v.id IN (SELECT related_record_id FROM tmp_pending_records) and v.capacity_assessments_states_id in (2,5)) or (v.capacity_assessments_states_id = 6 and v.user_session = v_id_user) THEN true
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
		
		
		
        WHERE (v_status = ARRAY[-1] OR v.capacity_assessments_states_id = ANY(v_status))
		AND (v.program_id = v_program OR v_program = -1)
        AND (im.acronym ILIKE '%' || filter || '%' OR v.code ILIKE '%' || filter || '%' OR filter = '')
        /*AND (v.travel_end_date >= start_date OR start_date IS NULL)
        AND (v.travel_start_date <= end_date OR end_date IS NULL)*/
        ORDER BY 
            -- Primero los viajes que están en tmp_viajes_pendientes
            pending_my_approval desc,
            -- Luego ordenar por id_viaje descendente
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


def downgrade():
    op.execute("""
    DROP FUNCTION IF EXISTS list_capacity_assesstment;
    """)