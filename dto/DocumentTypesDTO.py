from typing import Optional
from pydantic import BaseModel


class DocumentypesBase(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    code: Optional[str] = None

    class Config:
        from_attributes = True


class DocumentypeCreateBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    code: Optional[str] = None
