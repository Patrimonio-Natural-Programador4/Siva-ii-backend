
import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Text, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

from entity.controles import Controles

class AccesoControles(Base):
    __tablename__ = 'acceso_controles'
    __table_args__ = (
        ForeignKeyConstraint(['id_control'], ['controles.id_control'], name='acceso_controles_id_control_fkey'),
        ForeignKeyConstraint(['id_rol'], ['roles.id'], name='acceso_controles_id_rol_fkey'),
        PrimaryKeyConstraint('id_acceso_control', name='acceso_controles_pkey')
    )

    id_acceso_control: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_rol: Mapped[Optional[int]] = mapped_column(Integer)
    id_control: Mapped[Optional[int]] = mapped_column(Integer)
    acceso_control: Mapped[Optional[bool]] = mapped_column(Boolean)

    controles: Mapped[Optional['Controles']] = relationship('Controles')
#     roles: Mapped[Optional['Roles']] = relationship('Roles', back_populates='acceso_controles')
