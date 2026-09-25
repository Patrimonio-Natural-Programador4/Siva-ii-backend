from __future__ import annotations
import datetime
from typing import Optional

from sqlalchemy import BigInteger, DateTime, Integer, String, Text, PrimaryKeyConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class AgreementStages(Base):
    __tablename__ = 'agreement_stages'

    __table_args__ = (
        PrimaryKeyConstraint('id', name='agreement_stages_pkey'),
    )

    # ==============================================================================
    # 1. DEFINICIÓN DE COLUMNAS FÍSICAS (PostgreSQL Mapped Columns)
    # ==============================================================================
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    color: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'gray'::character varying"))
    stages_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    stage: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[Optional[str]] = mapped_column(String(255))
    order_colum: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    # ==============================================================================
    # 2. RELACIONES LÓGICAS (ORM)
    # ==============================================================================
    
 