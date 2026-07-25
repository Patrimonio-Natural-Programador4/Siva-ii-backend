
import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Text, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

from entity.modules import Modules


class ModuleAccess(Base):
    __tablename__ = 'module_access'

    __table_args__ = (
        ForeignKeyConstraint(
            ['module_id'],
            ['modules.id'],
            name='fk_module_access_module'
        ),
        ForeignKeyConstraint(
            ['role_id'],
            ['roles.id'],
            name='fk_module_access_role'
        ),
        PrimaryKeyConstraint(
            'module_access_id',
            name='module_access_pkey'
        )
    )

    module_access_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    role_id: Mapped[int] = mapped_column(Integer, nullable=False)
    module_id: Mapped[int] = mapped_column(Integer, nullable=False)

    has_access: Mapped[Optional[bool]] = mapped_column(Boolean)

    module: Mapped['Modules'] = relationship(
        'Modules',
        backref='module_access',
        lazy='joined'
    )