from pydantic import BaseModel
from typing import Optional

class DocumentoAsociadoCreate(BaseModel):
    nombre_original: str
    base64_data: str
    document_type_id: Optional[int] = None
    observaciones: Optional[str] = None

class DocumentoAsociadoResponse(BaseModel):
    id: int
    attachment_name: str
    document_type_id: Optional[int]
    observaciones: Optional[str]
    
    class Config:
        from_attributes = True
