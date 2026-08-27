from typing import Optional
from pydantic import BaseModel, Field

class Implementer_typesBase(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

    class Config:
        from_attributes = True

# DTO listar docs
class Implementer_typesListDTO(BaseModel):
    id: int
    name:str
    
    class Config:
        from_attributes = True

# DTO crear doc
class Implementer_typesCreateBase(BaseModel):
    name: str
   
    
# DTO editar doc
class Implementer_typesUpdateBase(BaseModel):
    name: str
   
