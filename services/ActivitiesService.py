import logging
from sqlalchemy.orm import Session

from dto.ActivitiesDTO import ActivitiesBase, ActivitiesListDTO

from dto.ResponseRequest import ResponseRequest
from entity.activities import Activities
from repository import ActivitiesRepository

def Activities_list(db: Session) -> list[ActivitiesBase]:
   
    activities = ActivitiesRepository.Activities_list(db)
    return [
        ActivitiesBase(
            id=int(a.id),
            activity_id=a.activity_id,
            code=a.code,
            description=a.description,
            pillar_id=a.pillar_id,
            is_logistics_expense_associate=a.is_logistics_expense_associate,
        )
        for a in activities
    ]

"""
def crear(payload: modalitiesCreateBase, db: Session) -> ResponseRequest:
    try:
        existente = PidsRepositoryy.obtener_por_nombre(payload.name or '', db)
        if existente:
            return ResponseRequest(mensaje='Ya existe una modalidad con ese nombre', solicitud_exitosa=False)

        nuevo = Modalities(name=(payload.name or '').strip())
        creado = PidsRepositoryy.crear(nuevo, db)
        return ResponseRequest(mensaje='Modalidad creada exitosamente', identity=int(creado.id), solicitud_exitosa=True)
    except Exception as e:
        logging.error(f"Error creating modality: {str(e)}")
        return ResponseRequest(mensaje='Error al crear la modalidad', solicitud_exitosa=False)
"""
