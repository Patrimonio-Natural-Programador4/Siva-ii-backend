import logging
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import text, or_, func, case
from entity.agreements import Agreements
from entity.priorities import Priorities
from entity.agreement_types import AgreementTypes
from entity.agreement_stages import AgreementStages
from entity.pillars import Pillars
from dto.AgreementsDTO import AgreementsListSP
from exceptions import PruebaNotFoundError


class AgreementsRepository:

    @staticmethod
    def obtener_pilares(db: Session):
        try:
            return (
                db.query(Pillars.id, Pillars.name, Pillars.color)
                .join(Agreements, Agreements.pillar_id == Pillars.id)
                .distinct()
                .order_by(Pillars.id.asc())
                .all()
            )
        except Exception as e:
            logging.error(f"Failed to fetch pillars: {str(e)}")
            raise PruebaNotFoundError(str(e))

    @staticmethod
    def obtener_anios_ejecucion(db: Session) -> List[int]:
        try:
            result = (
                db.query(Agreements.year)
                .filter(Agreements.year.isnot(None))
                .distinct()
                .order_by(Agreements.year.desc())
                .all()
            )
            return [row[0] for row in result if row[0] is not None]
        except Exception as e:
            logging.error(f"Failed to fetch execution years: {str(e)}")
            raise PruebaNotFoundError(str(e))

    @staticmethod
    def obtener_tipos(db: Session):
        try:
            return (
                db.query(AgreementTypes.id, AgreementTypes.name, AgreementTypes.color)
                .join(Agreements, Agreements.agreement_type_id == AgreementTypes.id)
                .filter(
                    or_(
                        Agreements.agreement_id.is_(None),
                        AgreementTypes.is_independent.is_(True)
                    )
                )
                .distinct()
                .order_by(AgreementTypes.name.asc())
                .all()
            )
        except Exception as e:
            logging.error(f"Failed to fetch agreement types: {str(e)}")
            raise PruebaNotFoundError(str(e))

    @staticmethod
    def obtener_fases(db: Session):
        try:
            return (
                db.query(
                    AgreementStages.name,
                    func.min(AgreementStages.id).label("id"),
                    func.min(AgreementStages.color).label("color")
                )
                .join(Agreements, Agreements.agreement_stage_id == AgreementStages.id)
                .filter(
                    AgreementStages.name.isnot(None),
                    func.trim(AgreementStages.name) != ''
                )
                .group_by(AgreementStages.name)
                .order_by(
                    case(
                        (AgreementStages.name == 'En Trámite', 1),
                        (AgreementStages.name == 'En ejecución', 2),
                        (AgreementStages.name == 'En elaboración', 3),
                        (AgreementStages.name == 'En liquidación', 4),
                        (AgreementStages.name == 'Liquidado', 5),
                        (AgreementStages.name == 'Suspendido', 6),
                        else_=7
                    ).asc(),
                    AgreementStages.name.asc()
                )
                .all()
            )
        except Exception as e:
            logging.error(f"Failed to fetch agreement stages: {str(e)}")
            raise PruebaNotFoundError(str(e))

    @staticmethod
    def obtener_prioridades(db: Session):
        try:
            return (
                db.query(Priorities.id, Priorities.name)
                .order_by(Priorities.id.asc())
                .all()
            )
        except Exception as e:
            logging.error(f"Failed to fetch priorities: {str(e)}")
            raise PruebaNotFoundError(str(e))

    @staticmethod
    def obtener_alertas(db: Session) -> List[str]:
        try:
            result = (
                db.query(Agreements.alert)
                .filter(
                    Agreements.alert.isnot(None),
                    func.trim(Agreements.alert) != ''
                )
                .group_by(Agreements.alert)
                .order_by(
                    case(
                        (Agreements.alert == 'Alta', 1),
                        (Agreements.alert == 'Media', 2),
                        (Agreements.alert == 'Baja', 3),
                        else_=4
                    ).asc()
                )
                .all()
            )
            return [row[0] for row in result if row[0] is not None]
        except Exception as e:
            logging.error(f"Failed to fetch alerts: {str(e)}")
            raise PruebaNotFoundError(str(e))

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
        p_page_size: int = 20
    ) -> List[AgreementsListSP]:
        try:
            result = db.execute(
                text("""
                    SELECT * FROM list_agreements(
                        :p_agreement_id,
                        :p_type_ids,
                        :p_modality_ids,
                        :p_pillar_ids,
                        :p_core_ids,
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
                    'p_pillar_ids': p_pillar_ids,
                    'p_core_ids': p_core_ids,
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
                AgreementsListSP(
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
                    total_records=row[20],
                    total_registros=row[20]
                )
                for row in result
            ]
            return convenios

        except Exception as e:
            logging.error(f"Failed to fetch Acuerdos: {str(e)}")
            raise PruebaNotFoundError(str(e))