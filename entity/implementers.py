import datetime
import uuid
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 

from sqlalchemy import BigInteger, Boolean, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

from entity.document_types import DocumentTypes
from entity.implementer_types import Implementer_types
from entity.capacity_assessments import CapacityAssessments

class Implementers(Base):
    __tablename__ = "implementers"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="implementers_pkey"),
        UniqueConstraint("acronym", name="acronym_unique"),
        Index("acronym_index", "acronym"),
        Index("nameee_index", "name"),
        #foranea
        ForeignKeyConstraint(
            ["identification_type"], #campo implemeners
            ["document_types.id"],
            name="implementers_document_types_fkey",
        ),
        ForeignKeyConstraint(
            ["type_id"],
            ["implementer_types.id"],
            name="implementers_implementer_types_fkey",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    acronym: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    identification_type: Mapped[int] = mapped_column(Integer, nullable=False)
    type_id: Mapped[int] = mapped_column(Integer, nullable=False)

    # RELACIONES ORM
    document_type: Mapped["DocumentTypes"] = relationship(
        "DocumentTypes", back_populates="implementers"
    )
    implementer_type: Mapped["Implementer_types"] = relationship(
        "Implementer_types", back_populates="implementers"
    )
    
    #Relaciones simples
    capacity_assessments_implementer:   Mapped[list["CapacityAssessments"]] = relationship("CapacityAssessments", back_populates="implementer") #este nombre debe coincidir con el del otro lado
  

    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))