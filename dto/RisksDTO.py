from typing import Optional
from pydantic import BaseModel


class RisksBase(BaseModel):
    id: Optional[int] = None
    risk: Optional[str] = None
    mitigation: Optional[str] = None
    previous_studies_id : Optional[int] = None

    class Config:
        from_attributes = True


class RisksCreateBase(BaseModel):
    risk: Optional[str] = None
    mitigation: Optional[str] = None
    previous_studies_id: Optional[int] = None   
