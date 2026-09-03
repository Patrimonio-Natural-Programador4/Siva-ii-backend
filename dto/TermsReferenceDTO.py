
import uuid

from typing import Any, Optional
import uuid
from datetime import date
from pydantic import BaseModel


class TdrFormField(BaseModel):
    id: int | None = None
    value: Any = None
    value_text: str | None = None
    name: str | None = None


class TermsReferenceCreate(BaseModel):
    terms_reference_id: Optional[int] = None
    guid: Optional[uuid.UUID] = None
    program_id: Optional[int] = None
    description: Optional[str] = None
    approval_flow_id: Optional[int] = None
    tdr_form: Optional[list[TdrFormField]] = None
