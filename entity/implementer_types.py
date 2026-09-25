import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Text, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

class Implementer_types(Base):
    __tablename__ = 'implementer_types'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='Implementer_types_pkey'),
        UniqueConstraint('name', name='Implementer_types_name_unique')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(CITEXT, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))


 # RELACIONES

    implementers: Mapped[list["Implementers"]] = relationship(
        "Implementers", back_populates="implementer_type"
    )
