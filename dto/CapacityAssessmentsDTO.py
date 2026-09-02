from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID

class CapacityAssessmentsBase(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    observation: Optional[str] = None
    approximate_value: Optional[int] = None
    guid: Optional[UUID] = None  
    user_session: Optional[int] = None
    create_date: Optional[datetime] = None
    policy_approval_date: Optional[date] = None
    document_signature_date: Optional[date] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    codigo: Optional[str] = None 
    programa: Optional[str] = None
    program_id: Optional[int] = None        
    pid: Optional[str] = None
    pid_id: Optional[int] = None             
    implementer: Optional[str] = None
    implementer_id: Optional[int] = None      
    aproval_request: Optional[str] = None
    approval_request_id:  Optional[int] = None
    person: Optional[str] = None
    persons_id: Optional[int] = None          
    capacity_assessments_state: Optional[str] = None
    capacity_assessments_states_id: Optional[int] = None  
    modality_id: Optional[int] = None        

    class Config:
        from_attributes = True



 #guid, 
 #user_session, 

class CapacityAssessmentsCreate(BaseModel):
    name: Optional[str] = None
    observation: Optional[str] = None
    approximate_value: Optional[int] = None
    policy_approval_date: Optional[date] = None
    document_signature_date: Optional[date] = None
    user_session:Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    create_date: Optional[datetime] = None
    program_id: Optional[int] = None
    code: Optional[str] = None
    pid_id: Optional[int] = None
    implementer_id: Optional[int] = None
    persons_id: Optional[int] = None
    capacity_assessments_states_id: Optional[int] = None
    modality_id: Optional[int] = None
    approval_request_id:  Optional[int] = None

    class Config:
        from_attributes = True


class CapacityAssessmentsListDTO(BaseModel):
    id:Optional[int] = None
    name:Optional[str] = None
    observation:Optional[str] = None
    approximate_value:Optional[int] = None
    guid:Optional[UUID] = None  
    user_session:Optional[int] = None
    create_date:Optional[datetime] = None
    policy_approval_date:Optional[datetime] = None
    document_signature_date:Optional[datetime] = None
    start_date:Optional[date] = None
    end_date:Optional[date] = None
    code:Optional[str] = None 
    programa: Optional[str] = None
    pid: Optional[str] = None
    implementer: Optional[str] = None
    aproval_request :   Optional[str] = None
    approval_request_id: Optional[int] = None 
    person :  Optional[str] = None
    capacity_assessments_state: Optional[str] = None
    capacity_assessment: Optional[str] = None
    
    class Config:
        from_attributes = True
   


class CapacityAssessmentListSP(BaseModel):
    guid: Optional[UUID] = None
    codigo: Optional[str] = None
    name: Optional[str] = None
    implementer_id: Optional[int] = None
    implementer_name: Optional[str] = None
    pending_my_approval: Optional[bool] = None
    capacity_assessments_id: Optional[int] = None
    approval_request_id: Optional[int] = None
    user_id: Optional[int] = None
    guid_msft: Optional[UUID] = None
    step_order_actual_request: Optional[int] = None
    guid_msft_adjustment: Optional[UUID] = None
    total_records: Optional[int] = None

    class Config:
        from_attributes = True
        
        
        
