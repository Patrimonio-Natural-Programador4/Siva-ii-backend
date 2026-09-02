import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Text, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

from entity.capacity_assessments import CapacityAssessments
from entity.previous_studies import PreviousStudies

class Programs(Base):
    __tablename__ = 'programs'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='programs_pkey'),
        UniqueConstraint('name', name='programs_name_unique')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(CITEXT, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(CITEXT)
    code: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))


 # RELACIONES
    documents_approval = relationship("DocumentsApproval", back_populates="programs")
    
# Relaciones simples
    capacity_assessments_programa:  Mapped[list["CapacityAssessments"]] = relationship("CapacityAssessments", back_populates="programa")
    previous_studies_programs: Mapped[list["PreviousStudies"]] = relationship("PreviousStudies", back_populates="programs")
