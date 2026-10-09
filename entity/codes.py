import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Text, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

#from entity.capacity_assessments import CapacityAssessments

class Codes(Base):
    __tablename__ = 'codes'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='codes'),
   
    )
   
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    code: Mapped[str] = mapped_column(String, nullable= True )
    origin: Mapped[str] = mapped_column(String, nullable= True )
        
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    
    #capacity_assessments_modalitie:  Mapped[list["CapacityAssessments"]] = relationship("CapacityAssessments", back_populates="modalitie") #este nombre debe coincidir con el del otro lado