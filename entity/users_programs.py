import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Text, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

from models import Programs, Users


class UsersPrograms(Base):
    __tablename__ = 'users_programs'
    __table_args__ = (
        ForeignKeyConstraint(['id_program'], ['programs.id'], name='users_programs_id_program_fkey'),
        ForeignKeyConstraint(['id_user'], ['users.id'], name='users_programs_id_user_fkey'),
        PrimaryKeyConstraint('id_usuario_programa', name='users_programs_pkey')
    )

    id_usuario_programa: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_program: Mapped[int] = mapped_column(Integer, nullable=False)
    id_user: Mapped[int] = mapped_column(Integer, nullable=False)

    programs: Mapped['Programs'] = relationship('Programs', back_populates='users_programs')
    users: Mapped['Users'] = relationship('Users', back_populates='users_programs')