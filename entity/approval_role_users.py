from __future__ import annotations
from typing import Optional, List, Any
from sqlalchemy import Integer, Date, Text, ForeignKeyConstraint, PrimaryKeyConstraint, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from database.database import Base
from sqlalchemy import Sequence, text
from sqlalchemy.orm import mapped_column, Mapped
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entity.users import Users
    from entity.approval_roles import ApprovalRole

class ApprovalRoleUser(Base):
    __tablename__ = 'approval_role_users'

    __table_args__ = (
        ForeignKeyConstraint(
            ['approval_role_id'],
            ['approval_roles.approval_role_id'],
            name='fk_approval_role_users_role'
        ),
        ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
            name='fk_approval_role_users_user'
        ),
        PrimaryKeyConstraint(
            'approval_role_user_id',
            name='approval_role_users_pkey'
        )
    )

    approval_role_user_id: Mapped[int] = mapped_column(
        Integer,
        Sequence('approval_role_users_approval_role_user_id_seq'),
        primary_key=True
    )

    approval_role_id: Mapped[int] = mapped_column(Integer)

    user_id: Mapped[int] = mapped_column(Integer)

    active: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        server_default=text('true')
    )

    user: Mapped["Users"] = relationship(
        'Users',
        foreign_keys=[user_id],
        lazy='joined'
    )

    approval_role: Mapped["ApprovalRole"] = relationship(
        "ApprovalRole",
        back_populates="role_users"
    )
