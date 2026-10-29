import logging
from sqlalchemy.orm import Session

from dto.RisksDTO import RisksBase, RisksCreateBase
from dto.ResponseRequest import ResponseRequest
from entity.risks import Risks
from repository import RisksRepository


def list_risks(db: Session) -> list[RisksBase]:
    risk = RisksRepository.list_risks(db)
    return [
        RisksBase(
            id=int(p.id),
            risk=p.risk,
            mitigation=p.mitigation,
            previous_studies_id=p.previous_studies_id,
            
        )
        for p in risk
    ]


def get_risk_by_id(id_risk: int, db: Session) -> RisksBase | None:
    risk = RisksRepository.get_risk_by_id(id_risk, db)
    if not risk:
        return None
    return RisksBase(
        id_risk=int(risk.id),
        risk=risk.risk,
        mitigation=risk.mitigation,
        previous_studies_id=risk.previous_studies_id,
        
    )


def create_risk(payload: RisksCreateBase, db: Session) -> ResponseRequest:
    try:
        existente = RisksRepository.get_risk_by_risk(payload.risk or '', db)
        if existente:
            return ResponseRequest(mensaje='Ya existe un riesgo con ese nombre', solicitud_exitosa=False)

        nuevo = Risks(
            risk=(payload.risk or '').strip(),
            mitigation=payload.mitigation,
            previous_studies_id=payload.previous_studies_id,
            
        )
        creado = RisksRepository.create_risk(nuevo, db)
        return ResponseRequest(mensaje='Riesgo creado exitosamente', identity=int(creado.id), solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error creating risks: {str(e)}")
        return ResponseRequest(mensaje='Error al crear el riesgo', solicitud_exitosa=False)


def update_risk(id_risk: int, payload: RisksCreateBase, db: Session) -> ResponseRequest:
    try:
        risk = RisksRepository.get_risk_by_id(id_risk, db)
        if not risk:
            return ResponseRequest(mensaje='Riesgo no encontrado', solicitud_exitosa=False)

        nombre_nuevo = (payload.risk or '').strip()
        if nombre_nuevo.lower() != (risk.risk or '').lower():
            existente = RisksRepository.get_risk_by_risk(nombre_nuevo, db)
            if existente:
                return ResponseRequest(mensaje='Ya existe un riesgo con ese nombre', solicitud_exitosa=False)

        risk.risk = nombre_nuevo
        risk.mitigation = payload.mitigation
        risk.previous_studies_id = payload.previous_studies_id


        RisksRepository.update_risk(risk, db)
        return ResponseRequest(mensaje='riesgo actualizado exitosamente', identity=id_risk, solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error updating risk: {str(e)}")
        return ResponseRequest(mensaje='Error al actualizar el riesgo', solicitud_exitosa=False)


def list_risk_by_previous_study(id_previous_study: int, db:Session ):
    return(
        db.query(Risks).filter(Risks.previous_studies_id == id_previous_study).all()
        
    )