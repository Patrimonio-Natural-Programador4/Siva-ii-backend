import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Text, ForeignKeyConstraint, ForeignKey,Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

class Pads(Base):
    __tablename__ = "pads"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pads_pkey"),
        UniqueConstraint("name", name="pads_name_unique"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(CITEXT, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(CITEXT)
    color: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

    # RELACIONES
    pids: Mapped[list["Pids"]] = relationship("Pids", back_populates="pad")
    
    class Config:
        from_attributes = True