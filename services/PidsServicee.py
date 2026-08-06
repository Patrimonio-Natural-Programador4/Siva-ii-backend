import logging
from sqlalchemy.orm import Session

from dto.PidsDTO import PidsBase, PidsListDTO
from dto.ResponseRequest import ResponseRequest
from entity.Pidss import Pids
from repository import PidsRepositoryy

def listar(db: Session) -> list[PidsBase]:
    print("here in the service?")
    pids = PidsRepositoryy.listar(db)
    return [
        PidsBase(
            id=int(m.id),
            pad_id=int(m.pad_id),
            name=m.name,
            description = m.description,
            color= m.color,
            pad= m.pad.name if m.pad else None,
            eur_usd_rate = float(m.eur_usd_rate),
            usd_cop_rate = float(m.usd_cop_rate),
            eur_cop_rate = float(m.eur_cop_rate),
            sicof_code   = m.sicof_code
        )
        for m in pids
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
