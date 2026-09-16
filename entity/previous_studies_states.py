import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Text, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

#from entity.capacity_assessments import CapacityAssessments
from entity.previous_studies import PreviousStudies

class PreviousStudiesStates(Base):
    __tablename__ = 'previous_studies_states'
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    state: Mapped[str] = mapped_column(CITEXT, nullable=False)
    
 # RELACIONES
    
    previous_studies: Mapped[list["PreviousStudies"]] = relationship("PreviousStudies", back_populates="prev_studies_state") #este nombre debe coincidir con el del otro lado