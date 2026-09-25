import datetime
from typing import Optional

from sqlalchemy import BigInteger, ForeignKeyConstraint, PrimaryKeyConstraint, String, UniqueConstraint, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP
import decimal

class Regions(Base):
    __tablename__ = 'regions'
    __table_args__ = (
        ForeignKeyConstraint(['region_id'], ['regions.id'], name='regions_region_id_foreign'),
        PrimaryKeyConstraint('id', name='regions_pkey'),
        UniqueConstraint('region_id', 'name', name='regions_region_id_name_unique')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    code: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(CITEXT, nullable=False)
    region_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    description: Mapped[Optional[str]] = mapped_column(CITEXT)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    lat: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(7, 7))
    long: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(7, 7))

    region: Mapped[Optional['Regions']] = relationship('Regions', remote_side=[id])

