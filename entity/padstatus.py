import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Text, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

#from entity.capacity_assessments import CapacityAssessments

class PadStatus(Base):
    __tablename__ = 'padstatus'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='padstatus'),
   
    )
   

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(CITEXT, nullable= False )
    status: Mapped[bool] = mapped_column(Boolean, nullable= False )
   
   
    acquisitions_pad_status: Mapped[list["Acquisitions"]] = relationship("Acquisitions", back_populates="pad_status")
