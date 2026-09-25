from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class PersonBase(BaseModel):
     id:Optional[int] = None
     first_name:Optional[str] = None
     other_name:Optional[str] = None
     identification_type:Optional[int] = None
     last_name:Optional[str] = None
     other_last_name:Optional[str] = None
     email:Optional[str] = None
     phone:Optional[str] = None
     created_at:Optional[datetime] = None
     updated_at:Optional[datetime] = None
        
class Config:
        from_attributes = True

class PersonCreateBase(BaseModel):
    id:Optional[int] = None
    first_name:Optional[str] = None
    other_name:Optional[str] = None
    identification_type:Optional[int] = None
    last_name:Optional[str] = None
    other_last_name:Optional[str] = None
    email:Optional[str] = None
    phone:Optional[str] = None
    created_at:Optional[datetime] = None
    updated_at:Optional[datetime] = None
   
