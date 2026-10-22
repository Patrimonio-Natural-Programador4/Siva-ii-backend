from typing import Optional
from pydantic import BaseModel, Field


class PillarsBase(BaseModel):
    id:         Optional[int] = None
    name:       Optional[str] = None
    description:Optional[str] = None
    color:      Optional[str] = None
    person_id:  Optional[int] = None
    person:     Optional[str] = None
  
    class Config:
        from_attributes = True

# DTO listar docs
class PillarsListDTO(BaseModel):
    id:         Optional[int] = None
    name:       Optional[str] = None
    description:Optional[str] = None
    color:      Optional[str] = None
    person_id:  Optional[int] = None
    person:     Optional[str] = None
    
    class Config:
        from_attributes = True
