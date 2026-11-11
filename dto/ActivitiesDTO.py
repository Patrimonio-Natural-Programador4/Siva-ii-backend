from typing import Optional
from pydantic import BaseModel, Field


class ActivitiesBase(BaseModel):
    id: Optional[int] = None
    activity_id: Optional[int] = None
    code:  Optional[str] = None
    description:  Optional[str] = None
    pillar_id: Optional[int] = None
    is_logistics_expense_associate: Optional[bool]= None
    
    class Config:
        from_attributes = True

# DTO listar activities
class ActivitiesListDTO(BaseModel):
   id: Optional[int] = None
   activity_id: Optional[int] = None
   code:  Optional[str] = None
   description:  Optional[str] = None
   pillar_id: Optional[int] = None
   is_logistics_expense_associate: Optional[bool]= None
    
   class Config:
        from_attributes = True
