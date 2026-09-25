from __future__ import annotations
import datetime
from typing import Optional, Any

from sqlalchemy import BigInteger, Boolean, DateTime, String, Text, PrimaryKeyConstraint, JSON, text
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class AgreementTypes(Base):
    __tablename__ = 'agreement_types'

    __table_args__ = (
        PrimaryKeyConstraint('id', name='agreement_types_pkey'),
    )

    # ==============================================================================
    # 1. DEFINICIÓN DE COLUMNAS FÍSICAS (PostgreSQL Mapped Columns)
    # ==============================================================================
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    code: Mapped[Optional[str]] = mapped_column(String(15))
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_frame: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))
    is_independent: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))
    color: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'yellow'::character varying"))
    allowed_types: Mapped[Optional[Any]] = mapped_column(JSON)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    # ==============================================================================
    # 2. RELACIONES LÓGICAS (ORM)
    # ==============================================================================