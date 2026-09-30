from pydantic import BaseModel
from typing import Optional

class AttachmentAgreementCreate(BaseModel):
    attachment_name: str # nombre archivo
    base64_data: str  # archivo
    documents_types_agreements_id: Optional[int] = None
    observations: Optional[str] = None

class AttachmentAgreementResponse(BaseModel):
    id: int
    attachment_name: str # nombre archivo
    documents_types_agreements_id: Optional[int] 
    observations: Optional[str]
    
    class Config:
        from_attributes = True
