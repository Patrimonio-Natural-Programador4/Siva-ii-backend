from __future__ import annotations
import decimal
from typing import Optional
from sqlalchemy import Integer, Date, Text, ForeignKey, Numeric, String, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship
import datetime
from database.database import Base

from entity.travel_requests import TravelRequests
from entity.regimen_types import RegimenType

class TravelLegalization(Base):
    __tablename__ = 'travel_legalizations'
    __table_args__ = {'info': {'managed_by_alembic': True}}
    
    legalization_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    travel_request_id: Mapped[int] = mapped_column(Integer, ForeignKey('travel_requests.travel_request_id'), nullable=False)
    check_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    check_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    beneficiary: Mapped[str] = mapped_column(String(255), nullable=False)
    nit_beneficiary: Mapped[str] = mapped_column(String(20), nullable=False)
    observations_outlay: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    regimen_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('regimen_types.id'), nullable=False)
    subtotal: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    iva: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    retention_porcentage: Mapped[decimal.Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    retention: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    amount_paid: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    observations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today, nullable=False)

    travel_request: Mapped['TravelRequests'] = relationship('TravelRequests')
    regimen_type: Mapped['RegimenType'] = relationship('RegimenType')

    @property
    def regimen_name(self) -> Optional[str]:
        return self.regimen_type.name if self.regimen_type else None
