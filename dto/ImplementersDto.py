from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class ImplementerBase(BaseModel):
     id:Optional[int] = None
     acronym:Optional[str] = None
     name:Optional[str] = None
     identification_type:Optional[int] = None
     type_id:Optional[int] = None
     created_at:Optional[datetime] = None
     updated_at:Optional[datetime] = None
        
class Config:
        from_attributes = True

class ImplementerCreateBase(BaseModel):
    id:Optional[int] = None
    acronym:Optional[str] = None
    name:Optional[str] = None
    identification_type:Optional[int] = None
    type_id:Optional[int] = None
    created_at:Optional[datetime] = None
    updated_at:Optional[datetime] = None
   
