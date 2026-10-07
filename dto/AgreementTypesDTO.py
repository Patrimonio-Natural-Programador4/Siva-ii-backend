from typing import Optional
from pydantic import BaseModel


class AgreementTypesBase(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    is_frame: Optional[bool] = None
    is_independent: Optional[bool] = None
    color: Optional[str] = None
    #allowed_types: Optional[Any] = None

    class Config:
        from_attributes = True


class AgreementTypesCreateBase(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    is_frame: Optional[bool] = None
    is_independent: Optional[bool] = None
    color: Optional[str] = None     