import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Text, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint,Date, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

#from entity.approval_requests import ApprovalRequests 


class PreviousStudies(Base):
    __tablename__ = 'previous_studies'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='previous_studies_pkey'),
        
        #foranea
        ForeignKeyConstraint(["capacity_assessments_states_id"], ["capacity_assessments_states.id"],name="fk_previous_studies_capacity_assessments_states"),
        ForeignKeyConstraint(["approval_request_id"], ["approval_requests.approval_request_id"],name="fk_previous_studies_approval_request_fkey",),
        ForeignKeyConstraint(["implementer_id"], ["implementers.id"],name="fk_previous_studies_capacity_implementers"),
        ForeignKeyConstraint(["persons_id"], ["persons.id"],name="fk_previous_studies_assessment_persons"),
        ForeignKeyConstraint(["capacity_assessment_id"], ["capacity_assessments.id"],name="fk_previous_studies_capacity_assessment"),
        
        
    )

    id: Mapped[int] =       mapped_column(BigInteger, primary_key=True)
    precedents: Mapped[str] =     mapped_column(CITEXT, nullable=False)
    justification : Mapped[str] = mapped_column(CITEXT, nullable=False)
    scope : Mapped[str] = mapped_column(CITEXT, nullable=False)
    overall_objective : Mapped[str] = mapped_column(CITEXT, nullable=False)
    term : Mapped[str] = mapped_column(CITEXT, nullable=False)
    obligations : Mapped[str] = mapped_column(CITEXT, nullable=False)
    supervisor : Mapped[str] = mapped_column(CITEXT, nullable=False)
    user_session: Mapped[int] = mapped_column(BigInteger, nullable=False)
    create_date :  Mapped[Optional[datetime.date]] = mapped_column(Date)
    total_value : Mapped[int] = mapped_column(BigInteger, nullable=False)
    contributions_ei:Mapped[int] = mapped_column(BigInteger, nullable=False)
    total_value_executes_fpn: Mapped[int] = mapped_column(BigInteger, nullable=False)
    total_value_executes_ei: Mapped[int] = mapped_column(BigInteger, nullable=False)
    
    capacity_assessments_states_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    approval_request_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    implementer_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    persons_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    capacity_assessment_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
   
    
    contributions_fpn: Mapped[int] = mapped_column(BigInteger, nullable=False)
    estimated_term:Mapped[str] = mapped_column(CITEXT, nullable=False)
   
   #Relacion simples
    cap_assessments_state: Mapped["CapacityAssessmentsStates"] = relationship("CapacityAssessmentsStates", back_populates="previous_studies")
    app_request: Mapped["ApprovalRequests"] = relationship("ApprovalRequests", back_populates="previous_studies")
    implementers: Mapped["Implementers"] = relationship("Implementers", back_populates="previous_studies_implementer") #back populates debe coincidir con el nombre de la contraparte
    persons: Mapped["Persons"] = relationship("Persons", back_populates="previous_studies_person") 
    capacity_assessment: Mapped["CapacityAssessments"] = relationship("CapacityAssessments", back_populates="previous_studies_capacity_assessment") 
    
   