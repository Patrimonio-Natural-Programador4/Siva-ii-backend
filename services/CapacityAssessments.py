import logging
from sqlalchemy.orm import Session

from dto.CapacityAssessmentsDTO  import CapacityAssessmentsBase
from dto.ResponseRequest import ResponseRequest
from entity.implementers import Implementers
from repository import CapacityAssessments


def listar(db: Session) -> list[CapacityAssessmentsBase]:
    capacidades = CapacityAssessments.listar(db)
    return [
        CapacityAssessmentsBase(
            id=int(c.id),
            name=c.name,
            observation=c.observation,
            approximate_value=c.approximate_value,
            guid=c.guid,
            user_session=c.user_session,
            create_date=c.create_date,
            capacity_assessments_state=c.capacity_assessments_state.state if c.capacity_assessments_state else None,
            implementer=c.implementer.acronym if c.implementer.acronym else None,
            modalitie = c.modalitie.name if  c.modalitie.name else None,
            person = c.person.email if  c.person.email else None,
            pid = c.pid.name if  c.pid.name else None,
            programa = c.programa.name if  c.programa.name else None,
         
        )
        for c in capacidades
    ]