import logging
from sqlalchemy.orm import Session
from sqlalchemy import text
from dto.AgreementsDTO import AgreementItemDTO  # O el DTO de mapeo que uses en tu proyecto
from exceptions import PruebaNotFoundError  # Tu excepción personalizada
#from repository import AgreementItemsRepository # corrige agreementController

def listar_convenios_sp(
    db: Session,
    p_agreement_id: int = None,
    p_type_ids: list[int] = None,
    p_modality_ids: list[int] = None,
    p_core_ids: list[int] = None,
    p_pillar_ids: list[int] = None,
    p_years: list[int] = None,
    p_phase: list[str] = None,
    p_stage_ids: list[int] = None,
    p_priority: list[str] = None,
    p_alert: list[str] = None,
    p_search: str = None,
    p_page: int = 1,
    p_page_size: int = 25
) -> list[AgreementItemDTO]:
    try:
        result = db.execute(
            text("""
                SELECT * FROM public.list_agreements(
                    :p_agreement_id,
                    :p_type_ids,
                    :p_modality_ids,
                    :p_core_ids,
                    :p_pillar_ids,
                    :p_years,
                    :p_phase,
                    :p_stage_ids,
                    :p_priority,
                    :p_alert,
                    :p_search,
                    :p_page,
                    :p_page_size
                )
            """),
            {
                'p_agreement_id': p_agreement_id,
                'p_type_ids': p_type_ids,
                'p_modality_ids': p_modality_ids,
                'p_core_ids': p_core_ids,
                'p_pillar_ids': p_pillar_ids,
                'p_years': p_years,
                'p_phase': p_phase,
                'p_stage_ids': p_stage_ids,
                'p_priority': p_priority,
                'p_alert': p_alert,
                'p_search': p_search,
                'p_page': p_page,
                'p_page_size': p_page_size
            }
        ).fetchall()

        convenios = [
            AgreementItemDTO(
                id=row[0],
                codigo_siva=row[1],
                nombre_convenio=row[2],
                objeto_acuerdo=row[3],
                prioridad_acuerdo=row[4],
                ano_ejecucion=row[5],
                estado_name=row[6],
                estado_stage=row[7],
                estado_status=row[8],
                estado_color=row[9],
                tipo_name=row[10],
                tipo_color=row[11],
                modalidad_name=row[12],
                pilar_name=row[13],
                pilar_color=row[14],
                nucleos=row[15],
                implementadoras=row[16],
                monto_apropiado=row[17],
                monto_total_apropiado=row[18],
                total_paa=row[19],
                total_registros=row[20]
            )
            for row in result
        ]

        return convenios

    except Exception as e:
        logging.error(f"Failed to fetch Acuerdos: {str(e)}")
        raise PruebaNotFoundError(str(e))