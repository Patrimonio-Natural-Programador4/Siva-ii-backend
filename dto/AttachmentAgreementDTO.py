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
    document_type_description: Optional[str] = None
    observations: Optional[str]
    
    
class AttachmentAgreementUpdate(BaseModel):
    attachment_name: Optional[str] = None
    base64_data: Optional[str] = None
    documents_types_agreements_id: Optional[int] = None
    observations: Optional[str] = None
    
    class Config:
        from_attributes = True
