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

class TravelItineraries(Base):
    __tablename__ = 'travel_itineraries'
    __table_args__ = (
        ForeignKeyConstraint(['destination_municipality_id'], ['regions.id'], name='fk_travel_destination'),
        ForeignKeyConstraint(['origin_municipality_id'], ['regions.id'], name='fk_travel_origin'),
        ForeignKeyConstraint(['travel_request_id'], ['travel_requests.travel_request_id'], name='fk_travel_itinerary'),
        PrimaryKeyConstraint('travel_itinerary_id', name='travel_itineraries_pkey')
    )

    travel_itinerary_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    travel_request_id: Mapped[int] = mapped_column(Integer, nullable=False)
    travel_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    destination_municipality_id: Mapped[Optional[int]] = mapped_column(Integer)
    origin_municipality_id: Mapped[Optional[int]] = mapped_column(Integer)
    departure_time: Mapped[Optional[str]] = mapped_column(Text)
    comments: Mapped[Optional[str]] = mapped_column(Text)
    origin_village: Mapped[Optional[str]] = mapped_column(Text)
    destination_village: Mapped[Optional[str]] = mapped_column(Text)
    is_destination_village: Mapped[Optional[bool]] = mapped_column(Boolean)
    is_origin_village: Mapped[Optional[bool]] = mapped_column(Boolean)
    boarding_pass_path: Mapped[Optional[str]] = mapped_column(Text)
    boarding_pass_document: Mapped[Optional[str]] = mapped_column(Text)
    is_rural_area: Mapped[Optional[bool]] = mapped_column(Boolean)
    rural_area_comments: Mapped[Optional[str]] = mapped_column(Text)
    ticket_support_document: Mapped[Optional[str]] = mapped_column(Text)
    ticket_support_path: Mapped[Optional[str]] = mapped_column(Text)
    requires_air_tickets: Mapped[Optional[bool]] = mapped_column(Boolean)
    project_id: Mapped[Optional[int]] = mapped_column(Integer)
    budget_item_id: Mapped[Optional[int]] = mapped_column(Integer)

    destination_municipality: Mapped[Optional[Regions]] = relationship('Regions', foreign_keys=[destination_municipality_id])
    origin_municipality: Mapped[Optional[Regions]] = relationship('Regions', foreign_keys=[origin_municipality_id])

#     travel_request: Mapped['TravelRequests'] = relationship('TravelRequests', back_populates='travel_itineraries')

