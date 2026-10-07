from __future__ import annotations
import decimal
from typing import Optional
from sqlalchemy import ForeignKeyConstraint, Integer, Date, PrimaryKeyConstraint, Text, ForeignKey, Numeric, String, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship
import datetime
from database.database import Base

from entity.expense_advance_concepts import ExpenseAdvanceConcepts
from entity.travel_requests import TravelRequests
from entity.regimen_types import RegimenType



class TravelLegalizations(Base):
    __tablename__ = 'travel_legalizations'
    __table_args__ = (
        ForeignKeyConstraint(['concept_id'], ['expense_advance_concepts.expense_advance_concept_id'], name='travel_legalizations_concepts_fkey'),
        ForeignKeyConstraint(['regimen_type_id'], ['regimen_types.id'], name='travel_legalizations_regimen_type_id_fkey'),
        ForeignKeyConstraint(['travel_request_id'], ['travel_requests.travel_request_id'], name='travel_legalizations_travel_request_id_fkey'),
        PrimaryKeyConstraint('legalization_id', name='travel_legalizations_pkey')
    )

    legalization_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    travel_request_id: Mapped[int] = mapped_column(Integer, nullable=False)
    check_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    beneficiary: Mapped[str] = mapped_column(String(255), nullable=False)
    nit_beneficiary: Mapped[str] = mapped_column(String(20), nullable=False)
    regimen_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    subtotal: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    iva: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    retention_porcentage: Mapped[decimal.Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    retention: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    amount_paid: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    created_at: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today, nullable=False)
    check_number: Mapped[Optional[str]] = mapped_column(String(50))
    observations_outlay: Mapped[Optional[str]] = mapped_column(Text)
    observations: Mapped[Optional[str]] = mapped_column(Text)
    concept_id: Mapped[Optional[int]] = mapped_column(Integer)

    concept: Mapped[Optional['ExpenseAdvanceConcepts']] = relationship('ExpenseAdvanceConcepts')
    regimen_type: Mapped['RegimenType'] = relationship('RegimenType')
    travel_request: Mapped['TravelRequests'] = relationship('TravelRequests')
    # regimen_type: Mapped['RegimenType'] = relationship('RegimenType')

    # @property
    # def concept_name(self) -> Optional[str]:
    #     return self.concept.concept if self.concept else None
#     regimen_type: Mapped['RegimenTypes'] = relationship('RegimenTypes', back_populates='travel_legalizations')
#     travel_request: Mapped['TravelRequests'] = relationship('TravelRequests', back_populates='travel_legalizations')



#  @property
#     def regimen_name(self) -> Optional[str]:
#         return self.regimen_type.name if self.regimen_type else None