#from __future__ import annotations
#import datetime
#from typing import Optional

#from sqlalchemy import BigInteger, DateTime, String, Text, PrimaryKeyConstraint, text
#from sqlalchemy.orm import Mapped, mapped_column

#from database.database import Base


#class AgreementOrigins(Base):
#    __tablename__ = 'agreement_origins'

#    __table_args__ = (
#        PrimaryKeyConstraint('id', name='agreement_origins_pkey'),
    )

    # ==============================================================================
    # 1. DEFINICIÓN DE COLUMNAS FÍSICAS (PostgreSQL Mapped Columns)
    # ==============================================================================
#   id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#    name: Mapped[str] = mapped_column(Text, nullable=False)
#   description: Mapped[Optional[str]] = mapped_column(Text)
#    color: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'gray'::character varying"))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    # ==============================================================================
    # 2. RELACIONES LÓGICAS (ORM)
    # ==============================================================================
    