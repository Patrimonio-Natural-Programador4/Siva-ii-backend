from __future__ import annotations
from typing import Optional, List
from sqlalchemy import Integer, Text, ForeignKeyConstraint, PrimaryKeyConstraint, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from database.database import Base
from entity.programs import Programs
from sqlalchemy import text
from sqlalchemy.orm import mapped_column, Mapped
from entity.approval_categories import ApprovalCategory
from entity.approval_flow_steps import ApprovalFlowStep

class ApprovalFlow(Base):
    __tablename__ = 'approval_flows'

    __table_args__ = (
        ForeignKeyConstraint(
            ['category_id'],
            ['approval_categories.category_id'],
            name='fk_approval_flows_category'
        ),
        ForeignKeyConstraint(
            ['program_id'],
            ['programs.id'],
            name='approval_flows_program_id_fkey'
        ),
        PrimaryKeyConstraint(
            'approval_flow_id',
            name='approval_flows_pkey'
        )
    )

    approval_flow_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    name: Mapped[str] = mapped_column(Text)
    category_id: Mapped[int] = mapped_column(Integer)
    program_id: Mapped[Optional[int]] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(Text)
    active: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        server_default=text('true')
    )
    approval_with_advance: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        server_default=text('false')
    )
    supervisor_settlement_approval: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        server_default=text('false')
    )
    payment_approval: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        server_default=text('false')
    )
    category: Mapped[Optional["ApprovalCategory"]] = relationship(
        'ApprovalCategory',
        backref='approval_flows',
        lazy='joined'
    )
    program: Mapped[Optional["Programs"]] = relationship(
        'Programs',
        backref='approval_flows',
        lazy='joined'
    )
    steps: Mapped[List["ApprovalFlowStep"]] = relationship(
        "ApprovalFlowStep",
        back_populates="approval_flow",
        cascade="all, delete-orphan"
    )
    template: Mapped[Optional[str]] = mapped_column(Text)