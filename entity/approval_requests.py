from __future__ import annotations
import decimal
from typing import Optional, List, Any
from sqlalchemy import ARRAY, DateTime, Integer, Date, Text, ForeignKeyConstraint, PrimaryKeyConstraint,  Uuid, Boolean, Numeric, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import uuid
from database.database import Base
from sqlalchemy import Sequence, text
from sqlalchemy.orm import mapped_column, Mapped
from entity.approval_status import ApprovalStatus
from entity.previous_studies import PreviousStudies



class ApprovalRequests(Base):
    __tablename__ = 'approval_requests'
    __table_args__ = (
        ForeignKeyConstraint(['approval_status_id'], ['approval_status.approval_status_id'], name='fk_approval_request_status'),
        ForeignKeyConstraint(['approval_workflow_id'], ['approval_flows.approval_flow_id'], name='fk_approval_request_workflow'),
        PrimaryKeyConstraint('approval_request_id', name='approval_requests_pkey'),
        Index('idx_ar_related_record', 'related_record_id'),
        Index('idx_ar_workflow_status', 'approval_workflow_id', 'approval_status_id')
    )

    approval_request_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    approval_workflow_id: Mapped[Optional[int]] = mapped_column(Integer)
    approval_status_id: Mapped[Optional[int]] = mapped_column(Integer)
    requester_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    name: Mapped[Optional[str]] = mapped_column(Text)
    code: Mapped[Optional[str]] = mapped_column(Text)
    created_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    current_step: Mapped[Optional[int]] = mapped_column(Integer)
    related_record_id: Mapped[Optional[int]] = mapped_column(Integer)
    instrument_code: Mapped[Optional[str]] = mapped_column(Text)
    guid: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, server_default=text('gen_random_uuid()'))

    approval_status: Mapped[Optional['ApprovalStatus']] = relationship('ApprovalStatus')
#     approval_workflow: Mapped[Optional['ApprovalFlows']] = relationship('ApprovalFlows', back_populates='approval_requests')
#     approval_request_history: Mapped[list['ApprovalRequestHistory']] = relationship('ApprovalRequestHistory', back_populates='approval_request')

    capacity_assessments: Mapped[list["CapacityAssessments"]] = relationship(
            "CapacityAssessments", back_populates="approval_request")
    # capacity_assessments: Mapped[list["CapacityAssessments"]] = relationship(
    #         "CapacityAssessments", back_populates="approval_request"
    # )


    
    previous_studies: Mapped[list["PreviousStudies"]] = relationship("PreviousStudies", back_populates="app_request")



    #capacity_assessments: Mapped[list["CapacityAssessments"]] = relationship("CapacityAssessments", back_populates="approval_request")
   