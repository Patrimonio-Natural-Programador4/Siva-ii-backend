# ----------------------
# AgreementService.py 
# ---------------------
from typing import Optional, List
from sqlalchemy.orm import Session
from dto.AgreementsDTO import AgreementsListSP
from repository.AgreementsRepository import AgreementsRepository

class AgreementsService:

    @staticmethod
    def listar_convenios(
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
        """
        Lógica de negocio para obtener la lista filtrada de convenios.
        Invoca la ejecución del procedimiento almacenado a través de AgreementsRepository.
        """
        # Transformaciones, reglas de negocio
        return AgreementsRepository.listar_convenios_sp(
            db=db,
            p_agreement_id=p_agreement_id,
            p_type_ids=p_type_ids,
            p_modality_ids=p_modality_ids,
            p_core_ids=p_core_ids,
            p_pillar_ids=p_pillar_ids,
            p_years=p_years,
            p_phase=p_phase,
            p_stage_ids=p_stage_ids,
            p_priority=p_priority,
            p_alert=p_alert,
            p_search=p_search,
            p_page=p_page,
            p_page_size=p_page_size
        )