import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, ForeignKey, Text, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

from entity.capacity_assessments import CapacityAssessments
from entity.previous_studies import PreviousStudies

class Risks(Base):
    __tablename__ = 'risks'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='risks_pkey'),
       
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    risk: Mapped[str] = mapped_column(Text, nullable=False)
    mitigation: Mapped[str] = mapped_column(Text, nullable=False)
    previous_studies_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey('previous_studies.id'), nullable=True)
    
 # RELACIONES
    previous_study: Mapped[Optional["PreviousStudies"]] = relationship("PreviousStudies", back_populates="risks")   