from typing import Optional
from pydantic import BaseModel


class PreviousStudiesStatesBase(BaseModel):
    id: Optional[int] = None
    state: Optional[str] = None
    

    class Config:
        from_attributes = True


class PreviousStudiesStatesCreateBase(BaseModel):
    state: Optional[str] = None
    
