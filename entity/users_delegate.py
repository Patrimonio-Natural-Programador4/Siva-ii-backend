from __future__ import annotations
import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import BigInteger, ForeignKey, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database.database import Base

if TYPE_CHECKING:
    from entity.users import Users


class UsersDelegate(Base):
    __tablename__ = 'users_delegate'
    __table_args__ = {'info': {'managed_by_alembic': True}}

    delegation_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    responsable_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('users.id', name='fk_users_delegate_responsable'),
        nullable=False
    )
    delegate_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('users.id', name='fk_users_delegate_delegate'),
        nullable=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(precision=6),
        server_default=text('now()'),
        nullable=False
    )

    responsable: Mapped['Users'] = relationship('Users', foreign_keys=[responsable_id])
    delegate: Mapped['Users'] = relationship('Users', foreign_keys=[delegate_id])
