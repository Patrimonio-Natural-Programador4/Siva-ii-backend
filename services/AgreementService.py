import logging
from typing import Optional, List
from sqlalchemy.orm import Session
from dto.AgreementsDTO import AgreementsListSP
from dto.ListadosDTO import Listados
from dto.ListaGenerica import ListaGenerica
from repository.AgreementsRepository import AgreementsRepository
from repository.modalitiesRepository import listar as listar_modalidades
from entity.agreement_stages import AgreementStages
from exceptions import PruebaNotFoundError


class AgreementsService:

    @staticmethod
    def obtener_listados(db: Session) -> List[Listados]:
        try:
            listados: List[Listados] = []

            tipos = AgreementsRepository.obtener_tipos(db)
            lista_tipos = [
                ListaGenerica(
                    identity=row[0],
                    valor=row[1],
                    valor_referencia=row[2]
                )
                for row in tipos
            ]
            lista_tipos.append(
                ListaGenerica(
                    identity=0,
                    valor="Sin Tipo",
                    valor_referencia="neutral"
                )
            )

            listados.append(
                Listados(
                    id_listado=0,
                    tipo_listado="Tipos de Acuerdo",
                    lista_generica=lista_tipos
                )
            )
            modalidades = listar_modalidades(db)
            listados.append(
                Listados(
                    id_listado=1,
                    tipo_listado="Modalidades",
                    lista_generica=[
                        ListaGenerica(
                            identity=m.id,
                            valor=m.name
                        )
                        for m in modalidades
                    ]
                )
            )
            pilares = AgreementsRepository.obtener_pilares(db)
            listados.append(
                Listados(
                    id_listado=2,
                    tipo_listado="Pilares",
                    lista_generica=[
                        ListaGenerica(
                            identity=row[0],
                            valor=row[1],
                            valor_referencia=row[2]
                        )
                        for row in pilares
                    ]
                )
            )
            fases = AgreementsRepository.obtener_fases(db)
            listados.append(
                Listados(
                    id_listado=3,
                    tipo_listado="Fases",
                    lista_generica=[
                        ListaGenerica(
                            identity=row[1],
                            valor=row[0],
                            valor_referencia2=row[2]
                        )
                        for row in fases
                    ]
                )
            )
            anios = AgreementsRepository.obtener_anios_ejecucion(db)
            listados.append(
                Listados(
                    id_listado=4,
                    tipo_listado="Años",
                    lista_generica=[
                        ListaGenerica(
                            identity=a,
                            valor=str(a)
                        )
                        for a in anios
                    ]
                )
            )
            prioridades_db = AgreementsRepository.obtener_prioridades(db)
            listados.append(
                Listados(
                    id_listado=5,
                    tipo_listado="Prioridades",
                    lista_generica=[
                        ListaGenerica(
                            identity=row[0],
                            valor=row[1]
                        )
                        for row in prioridades_db
                    ]
                )
            )

            alertas_db = AgreementsRepository.obtener_alertas(db)
            listados.append(
                Listados(
                    id_listado=6,
                    tipo_listado="Alertas",
                    lista_generica=[
                        ListaGenerica(
                            identity=idx + 1,
                            valor=a
                        )
                        for idx, a in enumerate(alertas_db)
                    ]
                )
            )

            return listados

        except Exception as e:
            logging.error(f"Failed to fetch listados for agreements: {str(e)}")
            raise PruebaNotFoundError(str(e))

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
        p_page_size: int = 20
    ) -> List[AgreementsListSP]:

        if p_phase:
            todos_los_ids_por_fase = (
                db.query(AgreementStages.id)
                .filter(AgreementStages.name.in_(p_phase))
                .all()
            )
            ids_fase = [r[0] for r in todos_los_ids_por_fase if r[0] is not None]
            if ids_fase:
                p_stage_ids = list(set((p_stage_ids or []) + ids_fase))

        if p_stage_ids:
            nombres_etapas = (
                db.query(AgreementStages.name)
                .filter(AgreementStages.id.in_(p_stage_ids))
                .all()
            )
            nombres = [r[0] for r in nombres_etapas if r[0]]
            if nombres:
                todos_los_ids = (
                    db.query(AgreementStages.id)
                    .filter(AgreementStages.name.in_(nombres))
                    .all()
                )
                p_stage_ids = list(set([r[0] for r in todos_los_ids if r[0] is not None] + p_stage_ids))

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