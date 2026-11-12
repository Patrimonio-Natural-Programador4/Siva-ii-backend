from typing import Optional
from pydantic import BaseModel


class KfwObservationsBase(BaseModel):
    id: Optional[int] = None
    name: str
    
    
    

    class Config:
        from_attributes = True


class KfwObservationsCreateBase(BaseModel):
    name: str
   