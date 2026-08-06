import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Text, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

class CapacityAssessmentsStates(Base):
    __tablename__ = 'capacity_assessments_states'
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    state: Mapped[str] = mapped_column(CITEXT, nullable=False)
    
    
   

 # RELACIONES
   
