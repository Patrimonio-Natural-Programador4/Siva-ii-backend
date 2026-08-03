from typing import Optional
from pydantic import BaseModel, Field


class DocumentsApprovalBase(BaseModel):
    id: Optional[int] = None
    approval_category_id: Optional[int] = None
    program_id: Optional[int] = None
    documento: Optional[str] = None

    class Config:
        from_attributes = True

# DTO listar docs
class DocumentsApprovalListDTO(BaseModel):
    id: int
    documento: str
    categoria: str
    programa: str
    
    class Config:
        from_attributes = True

# DTO crear doc
class DocumentsCreateBase(BaseModel):
    documento: str
    approval_category_id: int
    program_id: int
    
# DTO editar doc
class DocumentsUpdateBase(BaseModel):
    documento: str
    approval_category_id: int
    program_id: int
