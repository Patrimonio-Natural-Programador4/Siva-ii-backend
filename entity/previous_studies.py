#ENTITY ESTUDIOS PREVIOS

import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, DateTime, Text, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint,Date, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP
from entity.implementers import Implementers
#from entity.capacity_assessments import CapacityAssessments


if TYPE_CHECKING:
    from entity.capacity_assessments import CapacityAssessments
    #from entity.approval_requests import ApprovalRequests
from entity.capacity_assessments import CapacityAssessments


class PreviousStudies(Base):
    __tablename__ = 'previous_studies'
    __table_args__ = (
        ForeignKeyConstraint(['agreement_type_id'], ['agreement_types.id'], name='fk_previous_studies_agreement_type_id'),
        ForeignKeyConstraint(['approval_request_id'], ['approval_requests.approval_request_id'], name='fk_previous_studies_approval_request'),
        ForeignKeyConstraint(['capacity_assessment_id'], ['capacity_assessments.id'], name='fk_previous_studies_capacity_assessments'),
        ForeignKeyConstraint(['implementer_id'], ['implementers.id'], name='fk_previous_studies_implemeters'),
        ForeignKeyConstraint(['modality_id'], ['modalities.id'], name='fk_previous_studies_modality_id'),
        ForeignKeyConstraint(['persons_id'], ['persons.id'], name='fk_previous_studies_persons'),
        ForeignKeyConstraint(['previous_studies_states_id'], ['previous_studies_states.id'], name='fk_previous_studies_previous_studies_states'),
        ForeignKeyConstraint(['program_id'], ['programs.id'], name='fk_previous_studies_programs'),
        PrimaryKeyConstraint('id', name='previous_studies_pkey')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    precedents: Mapped[str] = mapped_column(Text, nullable=False)
    justification: Mapped[Optional[str]] = mapped_column(Text)
    scope: Mapped[Optional[str]] = mapped_column(Text)
    overall_objective: Mapped[Optional[str]] = mapped_column(Text)
    term: Mapped[Optional[str]] = mapped_column(Text)
    obligations: Mapped[Optional[str]] = mapped_column(Text)
    supervisor: Mapped[Optional[str]] = mapped_column(Text)
    user_session: Mapped[Optional[int]] = mapped_column(BigInteger)
    create_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    total_value: Mapped[Optional[int]] = mapped_column(BigInteger)
    contributions_ei: Mapped[Optional[int]] = mapped_column(BigInteger)
    total_value_executes_fpn: Mapped[Optional[int]] = mapped_column(BigInteger)
    total_value_executes_ei: Mapped[Optional[int]] = mapped_column(BigInteger)
    implementer_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    persons_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    capacity_assessment_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    approval_request_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    contributions_fpn: Mapped[Optional[int]] = mapped_column(BigInteger)
    estimated_term: Mapped[Optional[str]] = mapped_column(Text)
    guid: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    program_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    code: Mapped[Optional[str]] = mapped_column(Text)
    previous_studies_states_id: Mapped[Optional[int]] = mapped_column(Integer)
    agreement_type_id: Mapped[Optional[int]] = mapped_column(Integer)
    modality_id: Mapped[Optional[int]] = mapped_column(Integer)

    app_request: Mapped["ApprovalRequests"] = relationship("ApprovalRequests", back_populates="previous_studies")
    implementers: Mapped["Implementers"] = relationship("Implementers") #back populates debe coincidir con el nombre de la contraparte
    persons: Mapped["Persons"] = relationship("Persons", back_populates="previous_studies_person") 
    capacity_assessment: Mapped["CapacityAssessments"] = relationship("CapacityAssessments") 
    programs:  Mapped["Programs"] = relationship("Programs", back_populates="previous_studies_programs")
    prev_studies_state: Mapped["PreviousStudiesStates"] = relationship("PreviousStudiesStates", back_populates="previous_studies")
    ##
    agreement_type: Mapped['AgreementTypes'] = relationship('AgreementTypes')
    modality: Mapped[Optional['Modalities']] = relationship('Modalities')
    disbursements: Mapped[list["Disbursement"]] = relationship("Disbursement")
    # agreement_products: Mapped[list["AgreementsProducts"]] = relationship("AgreementsProducts", back_populates="previous_study")
    risks: Mapped[list["Risks"]] = relationship("Risks", back_populates="previous_study")
