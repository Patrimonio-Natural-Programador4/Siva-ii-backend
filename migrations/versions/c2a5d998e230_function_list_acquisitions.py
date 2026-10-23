"""function list_acquisitions

Revision ID: c2a5d998e230
Revises: b27f29f35ae0
Create Date: 2026-10-23 12:37:05.216809

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2a5d998e230'
down_revision: Union[str, Sequence[str], None] = 'b27f29f35ae0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
                 DROP FUNCTION IF EXISTS public.list_acquisitions(
        integer, character varying, integer, integer, text[], text[], text[], text
    );
             """)
    
    op.execute("""
                 CREATE OR REPLACE FUNCTION public.list_acquisitions(page integer DEFAULT 1, filter character varying DEFAULT ''::character varying, v_pid integer DEFAULT '-1'::integer, v_activity integer DEFAULT '-1'::integer, v_process text[] DEFAULT NULL::text[], v_rubros text[] DEFAULT NULL::text[], v_rubros_cortos text[] DEFAULT NULL::text[], v_activity_code text DEFAULT NULL::text)
 RETURNS TABLE(id bigint, process_number text, pid_id bigint, pad_name text, pillar_id bigint, pillar_name text, activity_id bigint, activity_code text, activity_description text, code_siva text, implementer_name text, executer_name text, rubro_id bigint, rubro_name text, rubro_corto text, general_category_name text, expense_category_name text, purchase_type_name text, contracts_qty integer, detail text, code text, agreement_id bigint, cod_siva_acuerdo text, contract_id bigint, cod_siva_contrato text, observations text, status_id bigint, status_name text, kfw_name text, departamento text, municipio text, vereda text, policy_date date, start_contract_date date, finish_date date, end_contract_date date, final_date date, final_date_con date, liquidation_date date, early_settlement_date date, initial_budget_cop numeric, initial_budget_usd numeric, initial_budget_eur numeric, final_budget_cop numeric, final_budget_usd numeric, final_budget_eur numeric, appropriate numeric, appropriate_sicof numeric, appropriate_pending numeric, fulfilled numeric, execute_sicof numeric, unfulfilled numeric, value numeric, value_con numeric, total_final_value numeric, total_final_value_con numeric, can_delete boolean, grand_initial_budget_cop numeric, grand_initial_budget_usd numeric, grand_initial_budget_eur numeric, grand_final_budget_cop numeric, grand_final_budget_usd numeric, grand_final_budget_eur numeric, grand_appropriate numeric, grand_appropriate_sicof numeric, grand_appropriate_pending numeric, grand_fulfilled numeric, grand_execute_sicof numeric, grand_unfulfilled numeric, grand_value numeric, grand_value_con numeric, grand_total_final_value numeric, grand_total_final_value_con numeric, total_records bigint, page_initial_budget_cop numeric, page_initial_budget_usd numeric, page_initial_budget_eur numeric, page_final_budget_cop numeric, page_final_budget_usd numeric, page_final_budget_eur numeric, page_appropriate numeric, page_appropriate_sicof numeric, page_appropriate_pending numeric, page_fulfilled numeric, page_execute_sicof numeric, page_unfulfilled numeric, page_value numeric, page_value_con numeric, page_total_final_value numeric, page_total_final_value_con numeric)
 LANGUAGE plpgsql
AS $function$
  #variable_conflict use_column
  DECLARE
  v_offset INT;
    v_filter TEXT;
    v_act_code TEXT;
BEGIN
  v_offset :=(Greatest(page, 1) - 1) * 25;
  v_filter := TRIM(Coalesce(FILTER, ''));
  v_act_code := Nullif(TRIM(Coalesce(v_activity_code, '')), '');


  RAISE notice 'Filtros -> page: %, filter: %, pid: %, activity: %, activity_code: %, process: %, rubros: %, cortos: %',
  page, v_filter, v_pid, v_activity, v_act_code, v_process, v_rubros, v_rubros_cortos;


  RETURN QUERY
  WITH

  todas AS(
  SELECT
    a.id :: BIGINT AS id,
         a.process_number :: TEXT AS process_number,
         a.pid_id :: BIGINT AS pid_id,
         p.pad :: TEXT AS pad_name,
         act.pillar_id :: BIGINT AS pillar_id,
         pl.NAME :: TEXT AS pillar_name,
         a.activity_id :: BIGINT AS activity_id,
         act.code :: TEXT AS activity_code,
         act.DESCRIPTION :: TEXT AS activity_description,
         a.code_siva :: TEXT AS code_siva,
         imp.acronym :: TEXT AS implementer_name,
         exe.acronym :: TEXT AS executer_name,
         a.rubro_id :: BIGINT AS rubro_id,
         ru.rubros :: TEXT AS rubro_name,
         COALESCE(
                NULLIF(ru.json_rubros::JSONB -> 0 -> 'rubros' ->> EXTRACT(YEAR FROM CURRENT_DATE)::TEXT, ''),
                NULLIF(ru.json_rubros::JSONB -> 0 -> 'rubros' ->> vig.max_year::TEXT, '')
            )::TEXT                                         AS rubro_corto,

         gc.NAME :: TEXT AS general_category_name,
         ec.NAME :: TEXT AS expense_category_name,
         pt.NAME :: TEXT AS purchase_type_name,
         a.contracts_qty :: INTEGER AS contracts_qty,
         a.detail :: TEXT AS detail,
         a.code :: TEXT AS code,
         a.agreement_id :: BIGINT AS agreement_id,
         Coalesce(ag.code, a.cod_siva_acuerdo) :: TEXT AS cod_siva_acuerdo,
         a.contractt_id :: BIGINT AS contract_id,
         Coalesce(co.code, a.cod_siva_contrato) :: TEXT AS cod_siva_contrato,
         a.observations :: TEXT AS observations,
         a.status_id :: BIGINT AS status_id,
         st.NAME :: TEXT AS status_name,
         kf.NAME :: TEXT AS kfw_name,
         reg.partes [2] :: TEXT AS departamento,
         reg.partes [3] :: TEXT AS municipio,
         Coalesce(reg.partes [4], ag.village) :: TEXT AS vereda,

         ag.policy_date :: DATE AS policy_date,
         co.start_contract_date :: DATE AS start_contract_date,
         ag.finish_date :: DATE AS finish_date,
         co.end_contract_date :: DATE AS end_contract_date,
         ag.final_date :: DATE AS final_date,
         co.final_date :: DATE AS final_date_con,
         ag.liquidation_date :: DATE AS liquidation_date,
         co.early_settlement_date :: DATE AS early_settlement_date,


         Round(Coalesce(a.initial_budget_cop, 0) :: NUMERIC, 2) AS initial_budget_cop,
         Round(Coalesce(a.initial_budget_usd, 0) :: NUMERIC, 2) AS initial_budget_usd,
         Round(Coalesce(a.initial_budget_eur, 0) :: NUMERIC, 2) AS initial_budget_eur,
         Round(Coalesce(a.final_budget_cop, 0) :: NUMERIC, 2) AS final_budget_cop,
         Round(Coalesce(a.final_budget_usd, 0) :: NUMERIC, 2) AS final_budget_usd,
         Round(Coalesce(a.final_budget_eur, 0) :: NUMERIC, 2) AS final_budget_eur,
         Round(Coalesce(a.appropriate, 0) :: NUMERIC, 2) AS appropriate,
         Round(Coalesce(sic_ap.apropiado, 0) :: NUMERIC, 2) AS appropriate_sicof,
         Round(Coalesce(a.appropriate_pending, 0) :: NUMERIC, 2) AS appropriate_pending,
         Round(Coalesce(a.fulfilled, 0) :: NUMERIC, 2) AS fulfilled,
         Round(Coalesce(sic_pay.pagado, 0) :: NUMERIC, 2) AS execute_sicof,
         Round(Coalesce(a.unfulfilled, 0) :: NUMERIC, 2) AS unfulfilled,
         Round(Coalesce(ag.VALUE, 0) :: NUMERIC, 2) AS VALUE,
         Round(Coalesce(co.VALUE, 0) :: NUMERIC, 2) AS value_con,


         -- Valor final del acuerdo: implementadoras + acuerdos hijos (adiciones)
         Round(
    CASE
    WHEN ag.id IS NULL THEN 0
    ELSE Coalesce(impl.total_implementadoras, 0)
    + Coalesce(adic.total_adiciones, 0)
    END :: NUMERIC, 2) AS total_final_value,


         -- Valor final del contrato: valor inicial + contratos hijos
         Round(
    CASE
    WHEN co.id IS NULL THEN 0
    ELSE Coalesce(co.initial_value, co.VALUE, 0)
    + Coalesce(hijos.total_hijos, 0)
    END :: NUMERIC, 2) AS total_final_value_con,


         -- Se puede eliminar si no tiene implementadoras, contratos ni notas
         (
    NOT EXISTS(SELECT 1
    FROM acquisition_implementer x
    WHERE x.acquisition_id = a.id)
    AND NOT EXISTS(SELECT 1
    FROM acquisition_contract x
    WHERE x.acquisition_id = a.id)
    AND NOT EXISTS(SELECT 1
    FROM notes x
    WHERE x.acquisition_id = a.id)
    ) :: BOOLEAN AS can_delete
  FROM acquisitions a
  LEFT JOIN pids p
  ON p.id = a.pid_id
  LEFT JOIN activities act
  ON act.id = a.activity_id
  LEFT JOIN pillars pl
  ON pl.id = act.pillar_id
  LEFT JOIN implementers imp
  ON imp.id = a.person_id_implementer
  LEFT JOIN implementers exe
  ON exe.id = a.person_id_executer
  LEFT JOIN rubros ru
  ON ru.id = a.rubro_id
  LEFT JOIN general_categories gc
  ON gc.id = a.general_cat_id
  LEFT JOIN expense_categories ec
  ON ec.id = a.expense_category_id
  LEFT JOIN purchase_types pt
  ON pt.id = a.purchase_type_id
  LEFT JOIN padstatus st
  ON st.id = a.status_id
  LEFT JOIN kfw_observations kf
  ON kf.id = a.kfw_id
  LEFT JOIN agreements ag
  ON ag.id = a.agreement_id
  LEFT JOIN contracts co
  ON co.id = a.contractt_id


    -- Suma de complementary_value de las implementadoras del acuerdo
  LEFT JOIN Lateral(
    SELECT SUM(ai.complementary_value) AS total_implementadoras
    FROM agreement_implementer ai
    WHERE ai.agreement_id = ag.id
    ) impl
  ON true


    -- Suma de los acuerdos hijos de tipo 12 (adiciones)
  LEFT JOIN Lateral(
    SELECT SUM(ah.VALUE) AS total_adiciones
    FROM agreements ah
    WHERE ah.agreement_id = ag.id
      AND ah.agreement_type_id = 12
    ) adic
  ON true


    -- Suma de los contratos hijos (adiciones del contrato)
  LEFT JOIN Lateral(
    SELECT SUM(ch.VALUE) AS total_hijos
    FROM contracts ch
    WHERE ch.contract_id = co.id
    ) hijos
  ON true


    -- Departamento / municipio / vereda 
  LEFT JOIN Lateral(
      WITH recursive subir AS(
      SELECT r.id,
             r.NAME,
             r.region_id,
             1 AS nivel
      FROM regions r
      WHERE r.id = ag.region_id
      UNION ALL
      SELECT r.id,
             r.NAME,
             r.region_id,
             s.nivel + 1
      FROM regions r
      INNER JOIN subir s
      ON r.id = s.region_id
      WHERE s.nivel < 10
      )
    SELECT Array_agg(s.NAME :: TEXT ORDER BY s.nivel DESC) AS partes
    FROM subir s
    ) reg ON true


    -- Año más alto con valor dentro de json_rubros (vigencia)
  LEFT JOIN Lateral(
    SELECT MAX(kv.KEY) :: INTEGER AS max_year
    FROM rubros r2
    CROSS JOIN lateral Jsonb_each_text((r2.json_rubros :: jsonb -> 0) -> 'rubros') AS kv
    WHERE r2.rubros = Coalesce(ru.rubros, a.rubro_id :: TEXT)
      AND kv.VALUE <> ''
    ) vig ON true


    -- SICOF: apropiado del año vigente
  LEFT JOIN Lateral(
    SELECT SUM(h.apropiation) AS apropiado
    FROM hws h
    WHERE h.rubro = Coalesce(ru.rubros, a.rubro_id :: TEXT)
      AND h.YEAR = Coalesce(vig.max_year, 0)
    ) sic_ap
  ON true


    -- SICOF: pagado de todos los años
  LEFT JOIN Lateral(
    SELECT SUM(h.ordinations) AS pagado
    FROM hws h
    WHERE h.rubro = Coalesce(ru.rubros, a.rubro_id :: TEXT)
    ) sic_pay
  ON true
  ),


 
  -- Totales generales 
  g AS(
  SELECT
    Round(SUM(t.initial_budget_cop), 2) AS grand_initial_budget_cop,
         Round(SUM(t.initial_budget_usd), 2) AS grand_initial_budget_usd,
         Round(SUM(t.initial_budget_eur), 2) AS grand_initial_budget_eur,
         Round(SUM(t.final_budget_cop), 2) AS grand_final_budget_cop,
         Round(SUM(t.final_budget_usd), 2) AS grand_final_budget_usd,
         Round(SUM(t.final_budget_eur), 2) AS grand_final_budget_eur,
         Round(SUM(t.appropriate), 2) AS grand_appropriate,
         Round(SUM(t.appropriate_sicof), 2) AS grand_appropriate_sicof,
         Round(SUM(t.appropriate_pending), 2) AS grand_appropriate_pending,
         Round(SUM(t.fulfilled), 2) AS grand_fulfilled,
         Round(SUM(t.execute_sicof), 2) AS grand_execute_sicof,
         Round(SUM(t.unfulfilled), 2) AS grand_unfulfilled,
         Round(SUM(t.VALUE), 2) AS grand_value,
         Round(SUM(t.value_con), 2) AS grand_value_con,
         Round(SUM(t.total_final_value), 2) AS grand_total_final_value,
         Round(SUM(t.total_final_value_con), 2) AS grand_total_final_value_con
  FROM todas t
  ),


  ids_filtrados AS(
  SELECT a.id
  FROM acquisitions a
  LEFT JOIN rubros ru
  ON ru.id = a.rubro_id
  LEFT JOIN activities act
  ON act.id = a.activity_id
  LEFT JOIN pids p
  ON p.id = a.pid_id
  LEFT JOIN implementers imp
  ON imp.id = a.person_id_implementer
  LEFT JOIN implementers exe
  ON exe.id = a.person_id_executer
  LEFT JOIN agreements ag
  ON ag.id = a.agreement_id
  LEFT JOIN contracts co
  ON co.id = a.contractt_id
  WHERE
    -- PAD
    (v_pid = -1 OR a.pid_id = v_pid)


    -- Actividad por id
    AND(v_activity = -1 OR a.activity_id = v_activity)


    -- Actividad 
    AND(v_act_code IS NULL OR act.code = v_act_code)


    -- Número de proceso 
    AND(v_process IS NULL OR Cardinality(v_process) = 0
    OR a.process_number :: TEXT = ANY(v_process))


    -- Rubro largo 
    AND(v_rubros IS NULL OR Cardinality(v_rubros) = 0
    OR ru.rubros = ANY(v_rubros))


    -- Rubro corto por vigencia 
    AND(v_rubros_cortos IS NULL OR Cardinality(v_rubros_cortos) = 0
    OR EXISTS(
    SELECT 1
    FROM Unnest(v_rubros_cortos) AS Rc(valor)
    WHERE CASE
      WHEN Position('||' IN rc.valor) > 0 THEN
       (ru.json_rubros :: jsonb -> 0 -> 'rubros' ->> Split_part(rc.valor, '||', 1))
      = Split_part(rc.valor, '||', 2)
      ELSE
      (ru.json_rubros :: jsonb -> 0 -> 'rubros' ->> EXTRACT(YEAR FROM current_date) :: TEXT)
      = rc.valor
      END
    ))


    -- barra
    AND(v_filter = ''
    OR a.process_number :: TEXT ilike '%' || v_filter || '%'
    OR a.code_siva ilike '%' || v_filter || '%'
    OR a.detail ilike '%' || v_filter || '%'
    OR a.observations ilike '%' || v_filter || '%'
    OR a.cod_siva_acuerdo ilike '%' || v_filter || '%'
    OR a.cod_siva_contrato ilike '%' || v_filter || '%'
    OR ru.rubros ilike '%' || v_filter || '%'
    OR act.code ilike '%' || v_filter || '%'
    OR act.DESCRIPTION ilike '%' || v_filter || '%'
    OR p.NAME ilike '%' || v_filter || '%'
    OR p.pad ilike '%' || v_filter || '%'
    OR imp.NAME ilike '%' || v_filter || '%'
    OR imp.acronym ilike '%' || v_filter || '%'
    OR exe.NAME ilike '%' || v_filter || '%'
    OR exe.acronym ilike '%' || v_filter || '%'
    OR ag.code ilike '%' || v_filter || '%'
    OR ag.NAME ilike '%' || v_filter || '%'
    OR co.code ilike '%' || v_filter || '%')
  ),


  pagina AS(
  SELECT
    t.*,
         g.*,
         COUNT(*) OVER() AS total_records
  FROM todas t
  CROSS JOIN g
  WHERE t.id IN(SELECT f.id
    FROM ids_filtrados f)
  ORDER BY t.id DESC
    limit CASE
    WHEN page = -1 THEN NULL
    ELSE 25
    END
    OFFSET CASE
    WHEN page = -1 THEN 0
    ELSE v_offset
    END
  )



SELECT
  pg.*,
       Round(SUM(pg.initial_budget_cop) OVER(), 2),
       Round(SUM(pg.initial_budget_usd) OVER(), 2),
       Round(SUM(pg.initial_budget_eur) OVER(), 2),
       Round(SUM(pg.final_budget_cop) OVER(), 2),
       Round(SUM(pg.final_budget_usd) OVER(), 2),
       Round(SUM(pg.final_budget_eur) OVER(), 2),
       Round(SUM(pg.appropriate) OVER(), 2),
       Round(SUM(pg.appropriate_sicof) OVER(), 2),
       Round(SUM(pg.appropriate_pending) OVER(), 2),
       Round(SUM(pg.fulfilled) OVER(), 2),
       Round(SUM(pg.execute_sicof) OVER(), 2),
       Round(SUM(pg.unfulfilled) OVER(), 2),
       Round(SUM(pg.VALUE) OVER(), 2),
       Round(SUM(pg.value_con) OVER(), 2),
       Round(SUM(pg.total_final_value) OVER(), 2),
       Round(SUM(pg.total_final_value_con) OVER(), 2)
FROM pagina pg
ORDER BY pg.id DESC;
  END;
$function$
   
                 """)

def downgrade() -> None:
    op.execute("""
        DROP FUNCTION IF EXISTS public.list_acquisitions(
            integer, character varying, integer, integer, text[], text[], text[], text
        );
    """)
