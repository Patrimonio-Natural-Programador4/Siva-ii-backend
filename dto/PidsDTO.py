from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class PidsBase(BaseModel):
     id:Optional[int] = None
     name:Optional[str] = None
     description:Optional[str] = None
     color:Optional[Decimal] = None
     eur_usd_rate:Optional[int] = None
     pad_id: Optional[int] = None
     pad:Optional[str] = None
     usd_cop_rate:Optional[Decimal] = None
     eur_cop_rate:Optional[Decimal] = None
     sicof_code:Optional[Decimal] = None
     created_at:Optional[datetime] = None
     updated_at:Optional[datetime] = None
        

class Config:
        from_attributes = True


class PidsCreateBase(BaseModel):
    name:Optional[str] = None
    description:Optional[str] = None
    color:Optional[Decimal] = None
    eur_usd_rate:Optional[int] = None
    pad_id: Optional[int] = None
    pad:Optional[str] = None
    usd_cop_rate:Optional[Decimal] = None
    eur_cop_rate:Optional[Decimal] = None
    sicof_code:Optional[Decimal] = None
    created_at:Optional[datetime] = None
    updated_at:Optional[datetime] = None
