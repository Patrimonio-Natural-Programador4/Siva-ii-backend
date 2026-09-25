# -------------------------------------------------------------------------------------------------------------------
# AgreementsRepository.py
# -------------------------------------------------------------------------------------------------------------------

import logging
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import text
from dto.AgreementsDTO import AgreementsListSP  
from dto.AgreementsDTO import AgreementsListSP  
from exceptions import PruebaNotFoundError  


class AgreementsRepository:

    @staticmethod
    def listar_convenios_sp(
        db: Session,
        p_agreement_id: Optional[int] = None,
        p_type_ids: Optional[List[int]] = None,
        p_modality_ids: Optional[List[int]] = None,
        p_core_ids: Optional[List[int]] = None,
        p_pillar_ids: Optional[List[int]] = None,
        p_years: Optional[List[int]] = None,
        p_phase: Optional[List[str]] = None,
        p_stage_ids: Optional[List[int]] = None,
        p_priority: Optional[List[str]] = None,
        p_alert: Optional[List[str]] = None,
        p_search: Optional[str] = None,
        p_page: int = 1,
        p_page_size: int = 25
    ) -> List[AgreementsListSP]:
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
            )

            # Mapeo dinámico por nombre de columna
            rows = result.mappings().all()
            return [AgreementsListSP(**row) for row in rows]

        except Exception as e:
            logging.error(f"Failed to fetch Acuerdos: {str(e)}")
            raise PruebaNotFoundError(str(e))
            
           