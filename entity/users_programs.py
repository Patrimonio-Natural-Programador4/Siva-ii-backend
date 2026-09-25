import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Text, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

from entity.programs import Programs
from entity.users import Users



class UsersPrograms(Base):
    __tablename__ = 'users_programs'
    __table_args__ = (
        ForeignKeyConstraint(['program_id'], ['programs.id'], name='users_programs_id_program_fkey'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='users_programs_id_user_fkey'),
        PrimaryKeyConstraint('user_program_id', name='users_programs_pkey')
    )

    user_program_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    program_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)

    programs: Mapped[Programs] = relationship('Programs')
    users: Mapped[Users] = relationship('Users')