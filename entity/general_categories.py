import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Text, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

#from entity.capacity_assessments import CapacityAssessments

class GeneralCategories(Base):
    __tablename__ = 'general_categories'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='general_categories'),
   
    )
   

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(CITEXT, nullable= False )
   
   
    acquisitions_general_categories: Mapped[list["Acquisitions"]] = relationship("Acquisitions", back_populates="general_categories")
