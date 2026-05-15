import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import BigInteger, Boolean, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP
from entity.role_has_permissions import t_role_has_permissions

if TYPE_CHECKING:
    from entity.roles import Roles


class Permissions(Base):
    __tablename__ = 'permissions'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='permissions_pkey'),
        UniqueConstraint('name', 'guard_name', name='permissions_name_guard_name_unique')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    guard_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    category: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    role: Mapped[list["Roles"]] = relationship('Roles', secondary=t_role_has_permissions, back_populates='permission')
    # model_has_permissions: Mapped[list['ModelHasPermissions']] = relationship('ModelHasPermissions', back_populates='permission')