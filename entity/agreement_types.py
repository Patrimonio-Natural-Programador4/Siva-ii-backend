import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Text, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

#from entity.capacity_assessments import CapacityAssessments

class AgreementTypes(Base):
    __tablename__ = 'agreement_types'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='agreement_types'),
   
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(CITEXT, nullable= False )
    code: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)    
    description: Mapped[str] = mapped_column(CITEXT, nullable= False )
    is_frame: Mapped[bool] = mapped_column(Boolean, nullable=False)   
    is_independent: Mapped[bool] = mapped_column(Boolean, nullable=False)   
    color: Mapped[str] = mapped_column(String(255), nullable=False)
    #allowed_types: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    

        
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    
    #capacity_assessments_modalitie:  Mapped[list["CapacityAssessments"]] = relationship("CapacityAssessments", back_populates="modalitie") #este nombre debe coincidir con el del otro lado