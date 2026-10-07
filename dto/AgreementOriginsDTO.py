from typing import Optional
from pydantic import BaseModel


class AgreementOriginsBase(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    color :    Optional[str] = None  

    class Config:
        from_attributes = True


class AgreementOriginsCreateBase(BaseModel):
     name: Optional[str] = None
     description: Optional[str] = None
     color :    Optional[str] = None  
