"""Actualizar función listar viajes

Revision ID: f67e554cd5d4
Revises: f4238ea967cc
Create Date: 2026-08-21 12:05:36.136158

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f67e554cd5d4'
down_revision: Union[str, Sequence[str], None] = 'f4238ea967cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    op.execute("""

    DROP FUNCTION IF EXISTS list_travels();

    CREATE OR REPLACE FUNCTION list_travels(
	guid_user_msft character varying,
	page integer DEFAULT 1,
	v_status integer[] DEFAULT ARRAY['-1'::integer],
	filter character varying DEFAULT ''::character varying,
	start_date date DEFAULT NULL::date,
	end_date date DEFAULT NULL::date,
	v_program integer DEFAULT '-1'::integer)
    RETURNS TABLE(guid uuid, code text, user_name text, created_at date, travel_start_date date, travel_end_date date, requires_advance_payment boolean, status text, status_id integer, pending_my_approval boolean, travel_request_id integer, expense_approval_request_id integer, approval_request_id integer, traveler_user_id integer, guid_msft uuid, step_order_actual_request integer, supervisor_approved boolean, guid_msft_adjustment uuid, days_since_completion integer, travel_expense_overdue text, program_name text, program_id integer, advance_amount numeric, total_records bigint) 
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
    AND c.code = 'ADM_VIA';

    -- Crear tabla temporal para viajes pendientes
    CREATE TEMPORARY TABLE tmp_pending_travels AS
    SELECT b.related_record_id
    FROM approval_request_history a
    INNER JOIN approval_requests b ON a.approval_request_id = b.approval_request_id
    INNER JOIN approval_flows c ON b.approval_workflow_id = c.approval_flow_id
    WHERE a.approval_status_id = 6
    AND a.user_id = v_id_user
    AND c.category_id IN (2);
	--2 = id_categoria aprobación viajes

    -- Insertar registros adicionales en la tabla de viajes pendientes
    INSERT INTO tmp_pending_travels
    SELECT b.related_record_id
    FROM approval_request_history a
    INNER JOIN approval_requests b ON a.approval_request_id = b.approval_request_id
    INNER JOIN approval_flows c ON b.approval_workflow_id = c.approval_flow_id
    INNER JOIN approval_role_users d ON a.approval_role_id = d.approval_role_id
    AND d.user_id = v_id_user
    WHERE a.approval_status_id = 6
    AND b.approval_status_id = 6
    AND d.user_id = v_id_user
	and a.user_id is null
    AND c.category_id IN (2);

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
            v.guid, v.code, a.full_name name, v.created_at::date, v.travel_start_date, v.travel_end_date, v.requires_advance_payment,
            --b.estado || ' ' || case when v.id_solicitud_aprobacion_legalizacion is null and v.id_solicitud_aprobacion is null then '' when v.id_solicitud_aprobacion_legalizacion is null and v.id_estado_solicitud in (2,3) then sv.responsable  when v.id_estado_solicitud in (5,6) then lv.responsable else '' end estado, 
			b.name as status, 
			b.status_id,
            CASE 
                WHEN (v.travel_request_id IN (SELECT related_record_id FROM tmp_pending_travels) and v.travel_status_id in (2,5)) or (v.travel_status_id = 6 and v.traveler_user_id = v_id_user) or (v.travel_status_id = 3 and guid_user_msft::UUID = case when v.expense_approval_request_id is null and v.approval_request_id is null then null when v.expense_approval_request_id is null then sv.guid_msft_adjustment  else lv.guid_msft_adjustment  end) THEN true
                ELSE false
            END AS pending_my_approval,
            v.travel_request_id,
			v.expense_approval_request_id, v.approval_request_id,
			v.traveler_user_id,
			a.guid_msft,
			case when v.expense_approval_request_id is null and v.approval_request_id is null then 0 when v.expense_approval_request_id is null then sv.step_order  else lv.step_order  end  step_order_actual_request,
			case when v.supervisor_approved is null then false else true end as supervisor_approved,
			case when v.expense_approval_request_id is null and v.approval_request_id is null then null when v.expense_approval_request_id is null then sv.guid_msft_adjustment  else lv.guid_msft_adjustment  end  guid_msft_adjustment,
			--case when v.pago_anticipo_rechazado is null then False else v.pago_anticipo_rechazado end as pago_anticipo_rechazado,
			days.working_days AS days_since_completion,
		    CASE 
		        WHEN b.status_id = 4 AND days.working_days > 5 
		            THEN 'SI'
		        ELSE 'NO'
		    END AS travel_expense_overdue,
			c.name::text as program_name,
			v.program_id,
			v.advance_amount,
			COUNT(*) OVER() AS total_records
        FROM travel_requests v
        INNER JOIN users a ON v.traveler_user_id = a.id
        INNER JOIN travel_status b ON v.travel_status_id = b.status_id
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
		
		--Legalización viaje
		LEFT JOIN LATERAL (
		    SELECT '(' || ra.name || ' - ' || COALESCE(us.full_name,'') || ')' as approver, fr.step_order,
			us.guid_msft as guid_msft_adjustment
		    FROM approval_request_history hi
			inner join approval_roles ra on hi.approval_role_id = ra.approval_role_id
			left join users us on hi.user_id = us.id
			left join approval_flow_steps fr on hi.step_id = fr.step_id
		    WHERE v.expense_approval_request_id = hi.approval_request_id
		    ORDER BY hi.history_id DESC
		    LIMIT 1
		) lv ON true
		CROSS JOIN LATERAL (
		    SELECT COUNT(*)::INTEGER AS working_days
		    FROM generate_series(v.travel_start_date::date, CURRENT_DATE, '1 day') AS g(dia)
		    WHERE EXTRACT(ISODOW FROM dia) < 6
		) AS days
        WHERE (v_status = ARRAY[-1] OR v.travel_status_id = ANY(v_status))
		AND (v.program_id = v_program OR v_program = -1)
        AND (a.full_name ILIKE '%' || filter || '%' OR v.code ILIKE '%' || filter || '%' OR filter = '')
        AND (v.travel_end_date >= start_date OR start_date IS NULL)
        AND (v.travel_start_date <= end_date OR end_date IS NULL)
        ORDER BY 
            -- Primero los viajes que están en tmp_viajes_pendientes
            pending_my_approval desc,
            -- Luego ordenar por id_viaje descendente
            v.travel_request_id DESC
        LIMIT 20 OFFSET (page - 1) * 20;
    ELSE
	RAISE NOTICE 'ENTRO 2: %', v_list_all_request;
        -- Si no hay "TS" ni "UBS", solo mostrar viajes relacionados con el usuario o viajes pendientes
        RETURN QUERY
        SELECT 
            v.guid, v.code, a.full_name name, v.created_at::date, v.travel_start_date, v.travel_end_date, v.requires_advance_payment,
            --b.estado || ' ' || case when v.id_solicitud_aprobacion_legalizacion is null and v.id_solicitud_aprobacion is null then '' when v.id_solicitud_aprobacion_legalizacion is null and v.id_estado_solicitud in (2,3) then sv.responsable  when v.id_estado_solicitud in (5,6) then lv.responsable else '' end estado, 
			b.name as status, 
			b.status_id,
            CASE 
                WHEN (v.travel_request_id IN (SELECT related_record_id FROM tmp_pending_travels) and v.travel_status_id in (2,5)) or (v.travel_status_id = 6 and v.traveler_user_id = v_id_user) or (v.travel_status_id = 3 and guid_user_msft::UUID = case when v.expense_approval_request_id is null and v.approval_request_id is null then null when v.expense_approval_request_id is null then sv.guid_msft_adjustment  else lv.guid_msft_adjustment  end) THEN true
                ELSE false
            END AS pending_my_approval,
            v.travel_request_id,
			v.expense_approval_request_id, v.approval_request_id,
			v.traveler_user_id,
			a.guid_msft,
			case when v.expense_approval_request_id is null and v.approval_request_id is null then 0 when v.expense_approval_request_id is null then sv.step_order  else lv.step_order  end  step_order_actual_request,
			case when v.supervisor_approved is null then false else true end as supervisor_approved,
			case when v.expense_approval_request_id is null and v.approval_request_id is null then null when v.expense_approval_request_id is null then sv.guid_msft_adjustment  else lv.guid_msft_adjustment  end  guid_msft_adjustment,
			--case when v.pago_anticipo_rechazado is null then False else v.pago_anticipo_rechazado end as pago_anticipo_rechazado,
			days.working_days AS days_since_completion,
		    CASE 
		        WHEN b.status_id = 4 AND days.working_days > 5 
		            THEN 'SI'
		        ELSE 'NO'
		    END AS travel_expense_overdue,
			c.name::text as program_name,
			v.program_id,
			v.advance_amount,
			COUNT(*) OVER() AS total_records
        FROM travel_requests v
        INNER JOIN users a ON v.traveler_user_id = a.id
        INNER JOIN travel_status b ON v.travel_status_id = b.status_id
		LEFT JOIN programs c on v.program_id = c.id
		LEFT JOIN LATERAL (
			SELECT '(' || ra.name || case when us.full_name is null then '' else  ' -> ' || us.full_name end ||')' as responsable, fr.step_order, us.guid_msft guid_msft_adjustment
		    FROM approval_request_history hi
			inner join approval_roles ra on hi.approval_role_id = ra.approval_role_id
			left join users us on hi.user_id = us.id
			left join approval_flow_steps fr on hi.step_id = fr.step_id
		    WHERE v.approval_request_id = hi.approval_request_id
		    ORDER BY hi.history_id DESC
		    LIMIT 1
		) sv ON true
		LEFT JOIN LATERAL (
		    SELECT '(' || ra.name || ' - ' || COALESCE(us.full_name,'') || ')' as approver, fr.step_order,
			us.guid_msft as guid_msft_adjustment
		    FROM approval_request_history hi
			inner join approval_roles ra on hi.approval_role_id = ra.approval_role_id
			left join users us on hi.user_id = us.id
			left join approval_flow_steps fr on hi.step_id = fr.step_id
		    WHERE v.expense_approval_request_id = hi.approval_request_id
		    ORDER BY hi.history_id DESC
		    LIMIT 1
		) lv ON true
		CROSS JOIN LATERAL (
		    SELECT COUNT(*)::INTEGER AS working_days
		    FROM generate_series(v.travel_start_date::date, CURRENT_DATE, '1 day') AS g(dia)
		    WHERE EXTRACT(ISODOW FROM dia) < 6
		) AS days
        WHERE v.traveler_user_id = v_id_user
        --OR v.travel_request_id IN (SELECT related_record_id FROM tmp_pending_travels)
        AND (v_status = ARRAY[-1] OR v.travel_status_id = ANY(v_status))
		AND (v.program_id = v_program OR v_program = -1)
        AND (a.full_name ILIKE '%' || filter || '%' OR v.code ILIKE '%' || filter || '%' OR filter = '')
        AND (v.travel_end_date >= start_date OR start_date IS NULL)
        AND (v.travel_start_date <= end_date OR end_date IS NULL)
        ORDER BY 
            -- Primero los viajes que están en tmp_viajes_pendientes
            pending_my_approval desc,
            -- Luego ordenar por id_viaje descendente
            v.travel_request_id DESC
        LIMIT 20 OFFSET (page - 1) * 20;
		RAISE NOTICE 'v_id_user: %', v_id_user;
		RAISE NOTICE 'v_program: %', v_program;
		RAISE NOTICE 'v_status: %', v_status;
		RAISE NOTICE 'filter: %', filter;
		RAISE NOTICE 'start_date: %', start_date;
		RAISE NOTICE 'end_date: %', end_date;
    END IF;
	drop table tmp_rol;
	drop table tmp_control;
	drop table tmp_pending_travels;
END;
$BODY$;



    """)


def downgrade():
    op.execute("""
    DROP FUNCTION IF EXISTS list_travels();
    """)