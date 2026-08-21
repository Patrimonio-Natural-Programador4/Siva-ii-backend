from typing import Optional
from pydantic import BaseModel


class ModalitiesBase(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

    class Config:
        from_attributes = True


class modalitiesCreateBase(BaseModel):
    name: Optional[str] = None
