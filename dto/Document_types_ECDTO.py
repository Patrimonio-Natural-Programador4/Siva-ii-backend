from typing import Optional
from pydantic import BaseModel


class Document_types_EC(BaseModel):
    resultado: Optional[str] = None

    class Config:
        from_attributes = True
