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


# Actualizar funcion List_agreements para migrar
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




#####

def downgrade():
    op.execute("""
    DROP FUNCTION IF EXISTS list_travels();
    """)