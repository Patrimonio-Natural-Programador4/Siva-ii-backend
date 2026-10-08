from typing import Optional
from pydantic import BaseModel


class CodesBase(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    origin: Optional[str] = None
    
    

    class Config:
        from_attributes = True


class CodesCreateBase(BaseModel):
    code: Optional[str] = None
    origin: Optional[str] = None
    