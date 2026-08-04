import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Text, ForeignKeyConstraint, Index, Integer,Numeric, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

class Pids(Base):
    __tablename__ = 'pids'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pids_pkey'),
        UniqueConstraint('name', name='pids_name_unique')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(CITEXT, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(CITEXT)
    color:Mapped[Optional[str]] = mapped_column(CITEXT)
    eur_usd_rate:Mapped[Optional[float]] = mapped_column(Numeric(12,6))
    pad_id:Mapped[int] = mapped_column(Integer, nullable=False)
    pad:Mapped[Optional[str]] = mapped_column(CITEXT)
    usd_cop_rate:Mapped[Optional[float]] = mapped_column(Numeric(12,6))
    eur_cop_rate:Mapped[Optional[float]] = mapped_column(Numeric(12,6))
    sicof_code:Mapped[Optional[str]] = mapped_column(CITEXT)
    created_at:Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    updated_at:Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
        
 

 # RELACIONES
    pads = relationship("pads", back_populates="pads")


