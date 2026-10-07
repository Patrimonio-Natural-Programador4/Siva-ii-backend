from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class AgreementStagesBase(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    stages_id: Optional[int] = None
    stage: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    order_colum: Optional[int] = None

    class Config:
        from_attributes = True

class AgreementStagesCreateBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    stages_id: Optional[int] = None
    stage: Optional[str] = None
    status: Optional[str] = None
    order_colum: Optional[int] = None