from __future__ import annotations
from typing import Optional, List, Any
from sqlalchemy import Integer, Date, Text, ForeignKeyConstraint, PrimaryKeyConstraint, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from database.database import Base
from sqlalchemy import Sequence, text
from sqlalchemy.orm import mapped_column, Mapped
from entity.approval_roles import ApprovalRole
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entity.approval_flows import ApprovalFlow
    
class ApprovalFlowStep(Base):
    __tablename__ = 'approval_flow_steps'

    __table_args__ = (
        ForeignKeyConstraint(
            ['approval_flow_id'],
            ['approval_flows.approval_flow_id'],
            name='fk_approval_flow_steps_flow'
        ),
        ForeignKeyConstraint(
            ['approval_role_id'],
            ['approval_roles.approval_role_id'],
            name='fk_approval_flow_steps_role'
        ),
        PrimaryKeyConstraint(
            'step_id',
            name='approval_flow_steps_pkey'
        )
    )

    step_id: Mapped[int] = mapped_column(
        Integer,
        Sequence('approval_flow_steps_step_id_seq'),
        primary_key=True
    )
    approval_flow_id: Mapped[int] = mapped_column(Integer)
    approval_role_id: Mapped[int] = mapped_column(Integer)
    step_order: Mapped[int] = mapped_column(Integer)
    active: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        server_default=text('true')
    )
    request_email_cc: Mapped[Optional[str]] = mapped_column(Text)
    adjustment_email_cc: Mapped[Optional[str]] = mapped_column(Text)
    approval_email_cc: Mapped[Optional[str]] = mapped_column(Text)
    assign_travel_budget: Mapped[Optional[bool]] = mapped_column(Boolean)
    adjust_travel_itinerary: Mapped[Optional[bool]] = mapped_column(Boolean)
    validate_supporting_documents: Mapped[Optional[bool]] = mapped_column(Boolean)
    validate_hotel_documents: Mapped[Optional[bool]] = mapped_column(Boolean)
    disable_advance_concepts: Mapped[Optional[bool]] = mapped_column(Boolean)
    add_rpc: Mapped[Optional[bool]] = mapped_column(Boolean)
    add_accounting_document: Mapped[Optional[bool]] = mapped_column(Boolean)
    add_medical_assistance_card: Mapped[Optional[bool]] = mapped_column(Boolean)
    add_expense_voucher: Mapped[Optional[bool]] = mapped_column(Boolean)
    send_payment_notification: Mapped[Optional[bool]] = mapped_column(Boolean)
    enable_payment: Mapped[Optional[bool]] = mapped_column(Boolean)
    enable_payment_rejection: Mapped[Optional[bool]] = mapped_column(Boolean)
    approval_flow: Mapped["ApprovalFlow"] = relationship(
        "ApprovalFlow",
        back_populates="steps"
    )
    approval_role: Mapped["ApprovalRole"] = relationship(
        "ApprovalRole",
        back_populates="steps"
    )