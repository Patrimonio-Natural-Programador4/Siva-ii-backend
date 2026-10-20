from typing import Optional
from pydantic import BaseModel


class DisbursementStateBase(BaseModel):
    id: Optional[int] = None
    name: str
    color: Optional[str] = None
    

    class Config:
        from_attributes = True


class DisbursementStateCreateBase(BaseModel):
    name: str
    color: Optional[str] = None
        
    
