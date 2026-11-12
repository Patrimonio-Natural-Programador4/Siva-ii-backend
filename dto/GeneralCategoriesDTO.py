from typing import Optional
from pydantic import BaseModel


class GeneralCategoriesBase(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    
    
    

    class Config:
        from_attributes = True


class GeneralCategoriesCreateBase(BaseModel):
    name: Optional[str] = None
    