from typing import Optional
from pydantic import BaseModel


class ContractTypesBase(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    #allowed_types: Optional[Any] = None

    class Config:
        from_attributes = True


class ContractTypesCreateBase(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None     