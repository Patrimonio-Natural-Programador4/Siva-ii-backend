import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Text, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

#from entity.capacity_assessments import CapacityAssessments

class KfwObservations(Base):
    __tablename__ = 'kfw_observations'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='kfw_observations'),
   
    )
   

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable= False )
    
   
   
    acquisitions_kfw_observations: Mapped[list["Acquisitions"]] = relationship("Acquisitions", back_populates="kfw_observations")
