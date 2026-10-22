import logging
from sqlalchemy.orm import Session

from dto.PillarsDTO  import PillarsBase, PillarsListDTO

from dto.ResponseRequest import ResponseRequest
#from entity.pillars import PillarssRepository
from repository import PillarssRepository


def _nombre_completo(p) -> str | None:
    if p is None:
        return None
    partes = [p.first_name, p.other_name, p.last_name, p.other_last_name]
    return " ".join(x.strip() for x in partes if x and x.strip())

def listar(db: Session) -> list[PillarsBase]:
    #print("here in the service?")
    pilars = PillarssRepository.listar(db)
    return [
        PillarsBase(
            id=int(m.id),
            name=m.name,
            description = m.description,
            color= m.color,
            person_id=m.person_id,
            person=_nombre_completo(m.person)
        )
        for m in pilars
    ]

