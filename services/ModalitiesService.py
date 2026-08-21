import logging
from sqlalchemy.orm import Session

from dto.modalitiesDTO import ModalitiesBase, modalitiesCreateBase
from dto.ResponseRequest import ResponseRequest
from entity.modalities import Modalities
from repository import modalitiesRepository


def listar_modalidades(db: Session) -> list[ModalitiesBase]:
    print("here in the service?")
    modalidades = modalitiesRepository.listar(db)
    return [
        ModalitiesBase(
            id=int(m.id),
            name=m.name,
        )
        for m in modalidades
    ]



def crear_modalidad (payload: modalitiesCreateBase, db: Session) -> ResponseRequest:
    try:
        existente = modalitiesRepository.obtener_por_nombre(payload.name or '', db)
        if existente:
            return ResponseRequest(mensaje='Ya existe una modalidad con ese nombre', solicitud_exitosa=False)

        nuevo = Modalities(name=(payload.name or '').strip())
        creado = modalitiesRepository.crear(nuevo, db)
        return ResponseRequest(mensaje='Modalidad creada exitosamente', identity=int(creado.id), solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error creating modality: {str(e)}")
        return ResponseRequest(mensaje='Error al crear la modalidad', solicitud_exitosa=False)

