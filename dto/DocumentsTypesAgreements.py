from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class DocumentsTypesAgreementsBase(BaseModel):
    
    id:Optional[int] = None
    is_required:    Optional[bool] = None        
    description:  Optional[str] = None
    number:  Optional[int] = None
    code:  Optional[str] = None
    template:  Optional[str] = None
    template_path:  Optional[str] = None
    is_active:   Optional[bool] = None
    documents_approval_id: Optional[int] = None
    documents_approval:   Optional[str] = None

        
class Config:
        from_attributes = True
        
# DTO crear tipo doc
class DocumentsTypesAgreementsCreateBase(BaseModel):
    id:Optional[int] = None
    is_required:    Optional[bool] = None        
    description:  Optional[str] = None
    number:  Optional[int] = None
    code:  Optional[str] = None
    template:  Optional[str] = None
    template_path:  Optional[str] = None
    is_active:   Optional[bool] = None
    documents_approval:   Optional[str] = None    
    

# DTO editar tipo doc
class DocumentsTypesAgreementsUpdateBase(BaseModel):
    is_required: Optional[bool] = None
    description: Optional[str] = None
    number: Optional[int] = None
    code: Optional[str] = None
    template: Optional[str] = None
    template_path: Optional[str] = None
    is_active: Optional[bool] = None
    documents_approval: Optional[str] = None

