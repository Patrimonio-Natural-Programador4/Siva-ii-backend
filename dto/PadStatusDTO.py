from typing import Optional
from pydantic import BaseModel


class PadStatusBase(BaseModel):
    id: Optional[int] = None
    name: str
    status: Optional[bool] = None
    
    

    class Config:
        from_attributes = True


class PadStatusCreateBase(BaseModel):
    name: str
    status: Optional[bool] = None