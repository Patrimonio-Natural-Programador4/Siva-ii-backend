from __future__ import annotations
from typing import Optional, List, Any
from sqlalchemy import Integer, Date, Text, ForeignKeyConstraint, PrimaryKeyConstraint, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from database.database import Base
from sqlalchemy import Sequence, text
from sqlalchemy.orm import mapped_column, Mapped
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entity.approval_role_users import ApprovalRoleUser
    from entity.approval_flow_steps import ApprovalFlowStep

class ApprovalRole(Base):
    __tablename__ = 'approval_roles'

    __table_args__ = (
        PrimaryKeyConstraint(
            'approval_role_id',
            name='approval_roles_pkey'
        ),
    )

    approval_role_id: Mapped[int] = mapped_column(
        Integer,
        Sequence('approval_roles_approval_role_id_seq'),
        primary_key=True
    )

    name: Mapped[str] = mapped_column(Text)

    description: Mapped[Optional[str]] = mapped_column(Text)

    active: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        server_default=text('true')
    )

    is_supervisor: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        server_default=text('false')
    )

    fcds_employees: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        server_default=text('false')
    )

    can_reject_payments: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        server_default=text('false')
    )

    role_users: Mapped[List["ApprovalRoleUser"]] = relationship(
        "ApprovalRoleUser",
        back_populates="approval_role",
        cascade="all, delete-orphan"
    )

    steps: Mapped[List["ApprovalFlowStep"]] = relationship(
        "ApprovalFlowStep",
        back_populates="approval_role"
    )