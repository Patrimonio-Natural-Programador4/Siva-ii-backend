from typing import Optional
from pydantic import BaseModel


class PurchaseTypesBase(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    origen: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    

    class Config:
        from_attributes = True


class PurchaseTypesCreateBase(BaseModel):
    name: Optional[str] = None
    origen: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None