import datetime
from typing import Optional
from sqlalchemy import BigInteger, Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

class Agreements(Base):
    __tablename__ = 'agreements'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='agreements_pkey'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    agreement_type_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    agreement_stage_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    agreement_origin_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    agreement_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    pillar_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    modality_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    name: Mapped[Optional[str]] = mapped_column(CITEXT)
    code: Mapped[Optional[str]] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(CITEXT)
    year: Mapped[Optional[int]] = mapped_column(Integer)
    priority: Mapped[Optional[str]] = mapped_column(String(255))
    alert: Mapped[Optional[str]] = mapped_column(String(40))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
