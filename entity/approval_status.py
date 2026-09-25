from typing import Optional
from sqlalchemy import Boolean, Integer, Text, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from database.database import Base

class ApprovalStatus(Base):
    __tablename__ = 'approval_status'
    __table_args__ = (
        PrimaryKeyConstraint('approval_status_id', name='approval_status_pkey'),
    )

    approval_status_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[str] = mapped_column(Text, nullable=False)
    code: Mapped[Optional[str]] = mapped_column(Text)

#     approval_requests: Mapped[list['ApprovalRequests']] = relationship('ApprovalRequests', back_populates='approval_status')
#     approval_request_history: Mapped[list['ApprovalRequestHistory']] = relationship('ApprovalRequestHistory', back_populates='approval_status')