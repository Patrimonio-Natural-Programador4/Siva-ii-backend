from typing import Optional
from pydantic import BaseModel


class PadsBase(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None

    class Config:
        from_attributes = True


class PadsCreateBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None

class PadsListDTO(BaseModel):
    id: int
    name: str
    description: str
    color: str
    
    class Config:
        from_attributes = True
