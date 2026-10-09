import datetime
from typing import Optional
from sqlalchemy import BigInteger, PrimaryKeyConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base
from sqlalchemy.dialects.postgresql import TIMESTAMP

class Priorities(Base):
    __tablename__ = 'priorities'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='priorities_pkey'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
