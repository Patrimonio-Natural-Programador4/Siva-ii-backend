import logging
from sqlalchemy.orm import Session

from dto.agreementStagesDTO import AgreementStagesBase, AgreementStagesCreateBase
from dto.ResponseRequest import ResponseRequest
from entity.agreement_stages import AgreementStages
from repository import AgreementStagesRepository


def listar(db: Session) -> list[AgreementStagesBase]:
    agrementStages = AgreementStagesRepository.listar(db)
    return [
        AgreementStagesBase(
            id=int(a.id),
            name=a.name,
            description=a.description,
            color=a.color,
            stage=a.stage,
            status=a.status,
            created_at=a.created_at,
            updated_at=a.updated_at,
            order_colum=a.order_colum,
        )
        for a in agrementStages
    ]

def obtener_pad_por_id(id: int, db: Session) -> AgreementStagesBase | None:
    agrementStage = AgreementStagesRepository.obtener_pad_por_id(id, db)
    if not agrementStage:
        return None
    return AgreementStagesBase(
        id=int(agrementStage.id),
        name=agrementStage.name,
        description=agrementStage.description,
        color=agrementStage.color,
        stage=agrementStage.stage,
        status=agrementStage.status,
        created_at=agrementStage.created_at,
        updated_at=agrementStage.updated_at,
        order_colum=agrementStage.order_colum,
    )