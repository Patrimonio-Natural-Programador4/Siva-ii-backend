from typing import Optional
from pydantic import BaseModel


class CapacityAssessmentsStatesBase(BaseModel):
    id: Optional[int] = None
    state: Optional[str] = None
    

    class Config:
        from_attributes = True


class CapacityAssessmentsStatesCreateBase(BaseModel):
    state: Optional[str] = None
    
