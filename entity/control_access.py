
import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Text, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

from entity.controls import Controls

class ControlAccess(Base):
    __tablename__ = 'control_access'

    __table_args__ = (
        ForeignKeyConstraint(
            ['control_id'],
            ['controls.control_id'],
            name='fk_control_access_control'
        ),
        ForeignKeyConstraint(
            ['role_id'],
            ['roles.id'],
            name='fk_control_access_role'
        ),
        PrimaryKeyConstraint(
            'control_access_id',
            name='control_access_pkey'
        )
    )

    control_access_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role_id: Mapped[Optional[int]] = mapped_column(Integer)
    control_id: Mapped[Optional[int]] = mapped_column(Integer)
    has_access: Mapped[Optional[bool]] = mapped_column(Boolean)

    control: Mapped[Optional['Controls']] = relationship('Controls')