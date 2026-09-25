from typing import Optional
from sqlalchemy import Boolean, Integer, Text, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from database.database import Base
from entity.modules import Modules

class Controls(Base):
    __tablename__ = 'controls'

    __table_args__ = (
        ForeignKeyConstraint(
            ['module_id'],
            ['modules.id'],
            name='fk_controls_module'
        ),
        PrimaryKeyConstraint(
            'control_id',
            name='controls_pkey'
        ),
        {
            "info": {
                "managed_by_alembic": True
            }
        }
    )

    control_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    code: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    module_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    requires_validation: Mapped[Optional[bool]] = mapped_column(
        Boolean
    )

    module: Mapped['Modules'] = relationship(
        'Modules'
    )
