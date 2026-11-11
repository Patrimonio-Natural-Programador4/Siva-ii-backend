import logging
from sqlalchemy.orm import Session

from dto.KfwObservationsDTO import KfwObservationsBase, KfwObservationsCreateBase
from dto.ResponseRequest import ResponseRequest
from entity.kfw_observations import KfwObservations
from repository import KfwObservationsRepository


def list_kfw_observations(db: Session) -> list[KfwObservationsBase]:
    kfw_observations = KfwObservationsRepository.list_kfw_observations(db)
    return [
        KfwObservationsBase(
            id=int(m.id),
            name= m.name,
           
            
        )
        for m in kfw_observations
    ]



def create_kfw_observations(payload: KfwObservationsCreateBase, db: Session) -> ResponseRequest:
    try:
        existente = KfwObservationsRepository(payload.name or '', db)
        if existente:
            return ResponseRequest(mensaje='Ya existe un kfw con ese nombre', solicitud_exitosa=False)

        nuevo = KfwObservations(name=(payload.name or '').strip())
        creado = KfwObservationsRepository.create_kfw_observations(nuevo, db)
        return ResponseRequest(mensaje='Kfw creado exitosamente', identity=int(creado.id), solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error creating kfw : {str(e)}")
        return ResponseRequest(mensaje='Error al crear Kfw ', solicitud_exitosa=False)

