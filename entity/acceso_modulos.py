
import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Text, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

from entity.modules import Modules


class AccesoModulos(Base):
    __tablename__ = 'acceso_modulos'
    __table_args__ = (
        ForeignKeyConstraint(['id_modulo'], ['modules.id'], name='acceso_modulos_id_modulo_fkey'),
        ForeignKeyConstraint(['id_rol'], ['roles.id'], name='acceso_modulos_id_rol_fkey'),
        PrimaryKeyConstraint('id_acceso_modulo', name='acceso_modulos_pkey')
    )

    id_acceso_modulo: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_rol: Mapped[int] = mapped_column(Integer, nullable=False)
    id_modulo: Mapped[int] = mapped_column(Integer, nullable=False)
    acceso_modulo: Mapped[Optional[bool]] = mapped_column(Boolean)

    modules: Mapped['Modules'] = relationship('Modules', backref='acceso_modulos', lazy='joined')
    # roles: Mapped['Roles'] = relationship('Roles', back_populates='acceso_modulos')
