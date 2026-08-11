import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Text, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint,Date, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

from entity.approval_requests import ApprovalRequests 


class CapacityAssessments(Base):
    __tablename__ = 'capacity_assessments'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='CapacityAssessments_pkey'),
        Index("name_index_sessments", "name"),
        #foranea
        ForeignKeyConstraint
        (
            ["approval_request_id"], #campo capacity_assessments
            ["approval_requests.approval_request_id"],
            name="capacity_assessmentss_fkey",
        ),
        ForeignKeyConstraint(["capacity_assessments_states_id"], ["capacity_assessments_states.id"],name="fk_capacity_assessment_capacity_assessments_states"),
        ForeignKeyConstraint(["implementer_id"], ["implementers.id"],name="fk_capacity_assessment_capacity_implementers"),
        ForeignKeyConstraint(["modality_id"], ["modalities.id"],name="fk_capacity_assessment_modalities"),
        ForeignKeyConstraint(["persons_id"], ["persons.id"],name="fk_capacity_assessment_persons"),
        ForeignKeyConstraint(["pid_id"], ["pids.id"],name="fk_capacity_assessment_pids"),
        ForeignKeyConstraint(["program_id"], ["programs.id"],name="fk_capacity_assessment_programs"),
    )

    id: Mapped[int] =       mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] =     mapped_column(CITEXT, nullable=False)
    observation : Mapped[str] = mapped_column(CITEXT, nullable=False)
    approximate_value: Mapped[int] = mapped_column(BigInteger, nullable=False)

    guid: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    user_session: Mapped[int] = mapped_column(BigInteger, nullable=False)
    create_date :  Mapped[Optional[datetime.date]] = mapped_column(Date)
    approval_request_id: Mapped[int] = mapped_column(BigInteger, nullable=False) #importante
    capacity_assessments_states_id: Mapped[int] = mapped_column(BigInteger, nullable=False) #importante
    implementer_id: Mapped[int] = mapped_column(BigInteger, nullable=False) #importante
    modality_id: Mapped[int] = mapped_column(BigInteger, nullable=False) #importante
    persons_id: Mapped[int] = mapped_column(BigInteger, nullable=False) #importante
    pid_id: Mapped[int] = mapped_column(BigInteger, nullable=False) #importante
    program_id: Mapped[int] = mapped_column(BigInteger, nullable=False) #importante
    
    
    
    #created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    #updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    
    #Relaciones
    #approval_request: Mapped["ApprovalRequests"] = relationship(
    #     "ApprovalRequests", back_populates="capacity_assessments" #contrario
    )
    
    #Relacion simples
    capacity_assessments_state: Mapped["CapacityAssessmentsStates"] = relationship("CapacityAssessmentsStates", back_populates="capacity_assessments")
    implementer: Mapped["Implementers"] = relationship("Implementers", back_populates="capacity_assessments_implementer") #back populates debe coincidir con el nombre de la contraparte
    modalitie: Mapped["Modalities"] = relationship("Modalities", back_populates="capacity_assessments_modalitie") 
    person: Mapped["Persons"] = relationship("Persons", back_populates="capacity_assessments_person") 
    pid: Mapped["Pids"] = relationship("Pids", back_populates="capacity_assessments_pid") 
    programa: Mapped["Programs"] = relationship("Programs", back_populates="capacity_assessments_programa") 
    