from typing import Optional
from pydantic import BaseModel
from datetime import datetime,date
from decimal import Decimal
from uuid import UUID

class PreviousStudiesBase(BaseModel):
    id: Optional[int] = None
    precedents: Optional[str] = None
    justification: Optional[str] = None
    scope: Optional[str] = None
    overall_objective: Optional[str] = None
    term: Optional[str] = None
    obligations: Optional[str] = None
    supervisor: Optional[str] = None
    user_session: Optional[int] = None
    create_date: Optional[datetime] = None
    total_value: Optional[int] = None
    contributions_ei: Optional[int] = None
    total_value_executes_fpn: Optional[int] = None
    total_value_executes_ei: Optional[int] = None
    cap_assessments_state: Optional[str] = None
    app_request: Optional[str] = None
    implementers: Optional[str] = None
    persons: Optional[str] = None
    capacity_assessment: Optional[str] = None
    
    contributions_fpn: Optional[int] = None
    estimated_term: Optional[str] = None


    class Config:
        from_attributes = True

class PreviousStudiesCreateBase(BaseModel):
     id: Optional[int] = None
     precedents: Optional[str] = None
     justification: Optional[str] = None
     scope: Optional[str] = None
     overall_objective: Optional[str] = None
     term: Optional[str] = None
     obligations: Optional[str] = None
     supervisor: Optional[str] = None
     user_session: Optional[int] = None
     create_date: Optional[datetime] = None
     total_value: Optional[int] = None
     contributions_ei: Optional[int] = None
     total_value_executes_fpn: Optional[int] = None
     total_value_executes_ei: Optional[int] = None
     cap_assessments_state: Optional[int] = None
     implementer_id: Optional[str] = None
     persons_id: Optional[str] = None
     capacity_assessment: Optional[str] = None
     approval_request_id: Optional[int] = None
     contributions_fpn: Optional[int] = None
     estimated_term: Optional[str] = None
    

class PreviousStudiesListDTO(BaseModel):
    id: Optional[int] = None
    precedents: Optional[str] = None
    justification: Optional[str] = None
    scope: Optional[str] = None
    overall_objective: Optional[str] = None
    term: Optional[str] = None
    obligations: Optional[str] = None
    supervisor: Optional[str] = None
    user_session: Optional[int] = None
    create_date: Optional[datetime] = None
    total_value: Optional[int] = None
    contributions_ei: Optional[int] = None
    total_value_executes_fpn: Optional[int] = None
    total_value_executes_ei: Optional[int] = None
    cap_assessments_state: Optional[int] = None
    
    implementer_id: Optional[int] = None
    persons_id: Optional[int] = None
    capacity_assessment: Optional[int] = None
    approval_request_id: Optional[int] = None
    contributions_fpn: Optional[int] = None
    estimated_term: Optional[str] = None
    
   
    
    class Config:
        from_attributes = True
   
