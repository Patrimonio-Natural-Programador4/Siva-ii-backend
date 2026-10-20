import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Text, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP



class DisbursementState(Base):
    __tablename__ = 'disbursement_state'
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    color: Mapped[Optional[str]] = mapped_column(Text)

 # RELACIONES
    disbursements: Mapped[list["Disbursement"]] = relationship("Disbursement", back_populates="disbursement_state") 