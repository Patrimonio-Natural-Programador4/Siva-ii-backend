from __future__ import annotations
import decimal
from typing import Optional
from sqlalchemy import ForeignKeyConstraint, Integer, Date, PrimaryKeyConstraint, Text, ForeignKey, Numeric, String, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship
import datetime
from database.database import Base

from entity.expense_advance_concepts import ExpenseAdvanceConcepts


class TravelAdvances(Base):
    __tablename__ = 'travel_advances'
    __table_args__ = (
        ForeignKeyConstraint(['expense_advance_concept_id'], ['expense_advance_concepts.expense_advance_concept_id'], name='travel_advances_expense_advance_concept_id_fkey'),
        ForeignKeyConstraint(['travel_request_id'], ['travel_requests.travel_request_id'], name='travel_advances_travel_request_id_fkey'),
        PrimaryKeyConstraint('travel_advance_id', name='travel_advances_pkey')
    )

    travel_advance_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    travel_request_id: Mapped[Optional[int]] = mapped_column(Integer)
    expense_advance_concept_id: Mapped[Optional[int]] = mapped_column(Integer)
    amount: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))
    observations: Mapped[Optional[str]] = mapped_column(Text)

    concept: Mapped[Optional['ExpenseAdvanceConcepts']] = relationship('ExpenseAdvanceConcepts')
    # travel_request: Mapped[Optional['TravelRequests']] = relationship('TravelRequests', back_populates='travel_advances')

