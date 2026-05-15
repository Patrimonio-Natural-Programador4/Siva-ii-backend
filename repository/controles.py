
import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Text, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

from entity.modules import Modules

class Controles(Base):
    __tablename__ = 'controles'
    __table_args__ = (
        ForeignKeyConstraint(['id_modulo'], ['modules.id'], name='fk_control_module'),
        PrimaryKeyConstraint('id_control', name='controles_pkey')
    )

    id_control: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[str] = mapped_column(Text, nullable=False)
    id_modulo: Mapped[int] = mapped_column(Integer, nullable=False)
    requiere_validacion: Mapped[Optional[bool]] = mapped_column(Boolean)

    modules: Mapped['Modules'] = relationship('Modules')