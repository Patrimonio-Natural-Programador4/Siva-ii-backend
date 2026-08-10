from typing import Optional
from pydantic import BaseModel

class RubrosListSP(BaseModel):
    rubro_id:  Optional[int] = None
    rubro: Optional[str] = None
    short_rubro: Optional[str] = None
    activity_id:  Optional[int] = None
    activity_code: Optional[str] = None
    activity_description: Optional[str] = None
    class Config:
        from_attributes = True