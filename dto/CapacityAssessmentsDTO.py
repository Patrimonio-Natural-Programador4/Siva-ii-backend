from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from uuid import UUID

class CapacityAssessmentsBase(BaseModel):
    id:Optional[int] = None
    name:Optional[str] = None
    observation:Optional[str] = None
    approximate_value:Optional[int] = None
    guid:Optional[UUID] = None  
    user_session:Optional[int] = None
    create_date:Optional[datetime] = None
    capacity_assessments_state: Optional[str] = None
    implementer: Optional[str] = None
    modalitie: Optional[str] = None
    person: Optional[str] = None
    pid: Optional[str] = None
    programa: Optional[str] = None
   
        
class Config:
        from_attributes = True

class CapacityAssessmentsCreateBase(BaseModel):
    id:Optional[int] = None
    name:Optional[str] = None
    observation:Optional[str] = None
    approximate_value:Optional[int] = None
    guid:Optional[UUID] = None  
    user_session:Optional[int] = None
    create_date:Optional[datetime] = None
    

class CapacityAssessmentsListDTO(BaseModel):
    id:Optional[int] = None
    name:Optional[str] = None
    observation:Optional[str] = None
    approximate_value:Optional[int] = None
    guid:Optional[UUID] = None  
    user_session:Optional[int] = None
    create_date:Optional[datetime] = None
    capacity_assessments_state: Optional[str] = None
    implementer: Optional[str] = None
    modalitie: Optional[str] = None
    person: Optional[str] = None
    pid: Optional[str] = None
    programa: Optional[str] = None
    
    class Config:
        from_attributes = True
   
