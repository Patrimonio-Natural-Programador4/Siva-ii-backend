from typing import Optional
import uuid
from pydantic import BaseModel, Field
from datetime import date
class UsuariosBase(BaseModel):
    guid: uuid.UUID
    guid_msft: Optional[uuid.UUID] = None
    first_name: str
    last_name: str
    identification_type: int
    identification_number: int
    email: str
    is_active: bool
    other_name: Optional[str] = None
    other_last_name: Optional[str] = None
    position: Optional[str] = None
    full_name: Optional[str] = None
    class Config:
        from_attributes = True

class UsuariosCreateBase(BaseModel):
    guid_msft: uuid.UUID | None = None
    guid: uuid.UUID | None = None
    full_name: Optional[str] = None
    email: Optional[str] = None


class UsuariosEdicionBase(BaseModel):
    guid: uuid.UUID
    first_name: str
    last_name: str
    identification_type: int
    identification_number: int
    email: str
    is_active: bool
    other_name: Optional[str] = None
    other_last_name: Optional[str] = None
    position: Optional[str] = None
    program_ids: list[int] = Field(default_factory=list)
    role_ids: list[int] = Field(default_factory=list)

    class Config:
        from_attributes = True


class UsuariosUpdateBase(BaseModel):
    first_name: str
    last_name: str
    identification_type: int
    identification_number: int
    email: str
    is_active: bool
    other_name: Optional[str] = None
    other_last_name: Optional[str] = None
    position: Optional[str] = None
    program_ids: list[int] = Field(default_factory=list)
    role_ids: list[int] = Field(default_factory=list)