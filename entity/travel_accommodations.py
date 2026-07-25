from __future__ import annotations
import decimal
from typing import Optional, List, Any
from sqlalchemy import ARRAY, DateTime, Integer, Date, Text, ForeignKeyConstraint, PrimaryKeyConstraint,  Uuid, Boolean, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import uuid
from database.database import Base
from sqlalchemy import Sequence, text
from sqlalchemy.orm import mapped_column, Mapped

from entity.regions import Regions


class TravelAccommodations(Base):
    __tablename__ = 'travel_accommodations'
    __table_args__ = (
        ForeignKeyConstraint(['travel_request_id'], ['travel_requests.travel_request_id'], name='fk_travel_accommodation'),
        ForeignKeyConstraint(['municipality_id'], ['regions.id'], name='travel_accommodations_municipality_id_fkey'),
        PrimaryKeyConstraint('travel_accommodation_id', name='travel_accommodations_pkey')
    )

    travel_accommodation_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    travel_request_id: Mapped[Optional[int]] = mapped_column(Integer)
    municipality_id: Mapped[Optional[int]] = mapped_column(Integer)
    comments: Mapped[Optional[str]] = mapped_column(Text)
    check_in_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    check_out_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    accommodation_type: Mapped[Optional[str]] = mapped_column(Text, comment='RZ = Rural Area, C = City')
    support_document: Mapped[Optional[str]] = mapped_column(Text)
    support_document_path: Mapped[Optional[str]] = mapped_column(Text)
    foundation_managed_payment: Mapped[Optional[bool]] = mapped_column(Boolean)
    project_id: Mapped[Optional[int]] = mapped_column(Integer)
    budget_item_id: Mapped[Optional[int]] = mapped_column(Integer)
    municipality: Mapped[Optional['Regions']] = relationship('Regions')
    # travel_request: Mapped[Optional['TravelRequests']] = relationship('TravelRequests', back_populates='travel_accommodations')
