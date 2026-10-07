from typing import Optional
from pydantic import BaseModel


class ProgramsBase(BaseModel):
    id_programa: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    code: Optional[str] = None
    first_alert_approval: Optional[int] = None
    secod_alert_approval: Optional[int] = None

    class Config:
        from_attributes = True


class ProgramsCreateBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    code: Optional[str] = None
    first_alert_approval: Optional[int] = None
    secod_alert_approval: Optional[int] = None
