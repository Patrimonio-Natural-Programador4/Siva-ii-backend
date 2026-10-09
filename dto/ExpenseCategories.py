from typing import Optional
from pydantic import BaseModel


class ExpenseCategoriesBase(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    
    

    class Config:
        from_attributes = True


class ExpenseCategoriesCreateBase(BaseModel):
    name: str
    description: Optional[str] = None
    