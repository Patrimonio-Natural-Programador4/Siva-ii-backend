from typing import Optional
from pydantic import BaseModel


class ProductsStateBase(BaseModel):
    id: Optional[int] = None
    name: str
    color: Optional[str] = None
    

    class Config:
        from_attributes = True


class ProductsStateCreateBase(BaseModel):
    name: str
    color: Optional[str] = None
        
    
