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

class ApprovalRequestHistory(Base):
    __tablename__ = 'approval_request_history'
    __table_args__ = (
        ForeignKeyConstraint(['approval_request_id'], ['approval_requests.approval_request_id'], name='fk_approval_request_history_request'),
        ForeignKeyConstraint(['approval_role_id'], ['approval_roles.approval_role_id'], name='fk_approval_request_history_role'),
        ForeignKeyConstraint(['approval_status_id'], ['approval_status.approval_status_id'], name='fk_approval_request_history_status'),
        ForeignKeyConstraint(['step_id'], ['approval_flow_steps.step_id'], name='fk_approval_request_history_route'),
        PrimaryKeyConstraint('history_id', name='approval_request_history_pkey'),
        Index('idx_arh_request', 'approval_request_id'),
        Index('idx_arh_role', 'approval_role_id'),
        Index('idx_arh_status_user', 'approval_status_id', 'user_id'),
        Index('idx_arh_user_status', 'user_id', 'approval_status_id')
    )

    history_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    approval_request_id: Mapped[int] = mapped_column(Integer, nullable=False)
    approval_role_id: Mapped[int] = mapped_column(Integer, nullable=False)
    approval_status_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    comments: Mapped[Optional[str]] = mapped_column(Text)
    step_id: Mapped[Optional[int]] = mapped_column(Integer)
    approved_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    received_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    due_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    mentioned_user_ids: Mapped[Optional[list[int]]] = mapped_column(ARRAY(Integer()))
    approver_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    approved_by_user: Mapped[Optional[str]] = mapped_column(Text)

    # approval_request: Mapped['ApprovalRequests'] = relationship('ApprovalRequests', back_populates='approval_request_history')
    # approval_role: Mapped['ApprovalRoles'] = relationship('ApprovalRoles', back_populates='approval_request_history')
    # approval_status: Mapped['ApprovalStatus'] = relationship('ApprovalStatus', back_populates='approval_request_history')
    # step: Mapped[Optional['ApprovalFlowSteps']] = relationship('ApprovalFlowSteps', back_populates='approval_request_history')