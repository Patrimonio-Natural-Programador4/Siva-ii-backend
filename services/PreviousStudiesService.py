import logging
from sqlalchemy.orm import Session

from dto.PreviousStudiesDTO import PreviousStudiesBase
from dto.ResponseRequest import ResponseRequest
from entity.implementers import Implementers
from repository import PreviousStudiesRepository


def listar(db: Session) -> list[PreviousStudiesBase]:
    estudios = PreviousStudiesRepository.listar(db)
    return [
       PreviousStudiesBase(
            id=int(e.id),
            precedents=e.precedents,
            justification=e.justification,
            scope=e.scope,
            overall_objective=e.overall_objective,
            term=e.term,
            obligations= e.obligations,
            supervisor = e.supervisor,
            user_session=e.user_session,
            create_date=e.create_date,
            total_value= e.total_value,
            contributions_ei= e.contributions_ei,
            total_value_executes_fpn=e.total_value_executes_fpn,
            total_value_executes_ei= e.total_value_executes_ei,
            contributions_fpn = e.contributions_fpn,
            estimated_term=e.estimated_term,           
            cap_assessments_state=e.cap_assessments_state.state if e.cap_assessments_state else None,
            app_request=e.app_request.name if e.app_request else None,
            implementers=e.implementers.acronym if e.implementers.acronym else None,
            persons = e.persons.email if  e.persons.email else None,
            capacity_assessment=e.capacity_assessment.name if  e.capacity_assessment.name else None,
            
        )
        for e in estudios
    ]