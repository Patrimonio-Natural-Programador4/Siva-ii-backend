import datetime
import uuid
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 

from sqlalchemy import BigInteger, Boolean, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, String,Date,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP


#from entity.implementer_types import Implementer_types

class DocumentsTypesAgreements(Base):
    __tablename__ = "documents_types_agreements"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="documents_types_agreements_pkey"),
        #UniqueConstraint("acronym", name="acronym_unique"),
        Index("description_index", "description"),
        Index("code_index", "code"),
       
    )
    
  
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    is_required: Mapped[bool] = mapped_column(Boolean, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    code: Mapped[str] = mapped_column(String, nullable=False)
    template: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    template_path: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    documents_approval_id: Mapped[int] = mapped_column(BigInteger,ForeignKey("documents_approval.id"))
        

   # RELACIONES ORM
  
    #documents_approval: Mapped["DocumentsApproval"] = relationship("DocumentsApproval",back_populates="documents_types_agreements")
    documents_approval: Mapped["DocumentsApproval"] = relationship("DocumentsApproval", back_populates="documents_types_agreements")

        