from __future__ import annotations
import decimal
from typing import Optional, List, Any
from sqlalchemy import ARRAY, DateTime, Integer, Date, Text, ForeignKeyConstraint, PrimaryKeyConstraint,  Uuid, Boolean, Numeric, CHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import uuid
from database.database import Base
from sqlalchemy import Sequence, text
from sqlalchemy.orm import mapped_column, Mapped

from entity.programs import Programs
from entity.travel_status import TravelStatus
from entity.users import Users
from entity.activities import Activities
from entity.rubros import Rubros

class TravelRequests(Base):
    __tablename__ = 'travel_requests'
    __table_args__ = (
        PrimaryKeyConstraint('travel_request_id', name='travel_requests_pkey'),
        ForeignKeyConstraint(['program_id'], ['programs.id'], name='travel_requests_program_id_fkey'),
        ForeignKeyConstraint(['traveler_user_id'], ['users.id'], name='travel_requests_traveler_user_id_fkey'),
        ForeignKeyConstraint(['travel_status_id'], ['travel_status.status_id'], name='travel_requests_travel_status_id_fkey'),
        ForeignKeyConstraint(['activity_id'], ['activities.id'], name='travel_requests_activities_fkey'),
        ForeignKeyConstraint(['rubro_id'], ['rubros.id'], name='travel_requests_rubros_fkey')
    )

    travel_request_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guid: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    code: Mapped[Optional[str]] = mapped_column(Text)
    traveler_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    travel_start_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    travel_end_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    activity_purpose: Mapped[Optional[str]] = mapped_column(Text)
    created_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    updated_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    account_number: Mapped[Optional[str]] = mapped_column(Text)
    account_type_id: Mapped[Optional[int]] = mapped_column(Integer)
    bank_id: Mapped[Optional[int]] = mapped_column(Integer)
    expense_report_submission_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    cancelled_at: Mapped[Optional[datetime.date]] = mapped_column(Date)
    cancellation_reason: Mapped[Optional[str]] = mapped_column(Text)
    cancelled_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    is_cancelled: Mapped[Optional[bool]] = mapped_column(Boolean)
    request_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    requires_advance_payment: Mapped[Optional[bool]] = mapped_column(Boolean)
    two_persons_travel: Mapped[Optional[bool]] = mapped_column(Boolean)
    is_workshop_related: Mapped[Optional[bool]] = mapped_column(Boolean)
    workshop_id: Mapped[Optional[int]] = mapped_column(Integer)
    travel_category_id: Mapped[Optional[int]] = mapped_column(Integer)
    total_hours: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))
    total_days: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))
    travel_status_id: Mapped[Optional[int]] = mapped_column(Integer)
    location_report: Mapped[Optional[str]] = mapped_column(Text)
    participating_institutions: Mapped[Optional[str]] = mapped_column(Text)
    topics_discussed: Mapped[Optional[str]] = mapped_column(Text)
    commitments: Mapped[Optional[str]] = mapped_column(Text)
    report_comments: Mapped[Optional[str]] = mapped_column(Text)
    approval_request_id: Mapped[Optional[int]] = mapped_column(Integer)
    is_guest: Mapped[Optional[bool]] = mapped_column(Boolean)
    guest_name: Mapped[Optional[str]] = mapped_column(Text)
    guest_document: Mapped[Optional[str]] = mapped_column(Text)
    guest_phone: Mapped[Optional[str]] = mapped_column(Text)
    guest_email: Mapped[Optional[str]] = mapped_column(Text)
    expense_approval_request_id: Mapped[Optional[int]] = mapped_column(Integer)
    requires_tickets: Mapped[Optional[bool]] = mapped_column(Boolean)
    is_international: Mapped[Optional[bool]] = mapped_column(Boolean)
    country: Mapped[Optional[str]] = mapped_column(Text)
    start_time: Mapped[Optional[str]] = mapped_column(Text)
    end_time: Mapped[Optional[str]] = mapped_column(Text)
    travel_type: Mapped[Optional[str]] = mapped_column(CHAR(1), comment='A = Air Travel, T = Ground Travel')
    traveler_birth_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    supervisor_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    supervisor_approval_role_id: Mapped[Optional[int]] = mapped_column(Integer)
    passport_support_document: Mapped[Optional[str]] = mapped_column(Text)
    passport_support_path: Mapped[Optional[str]] = mapped_column(Text)
    medical_assistance_document: Mapped[Optional[str]] = mapped_column(Text)
    medical_assistance_path: Mapped[Optional[str]] = mapped_column(Text)
    budget_item_id: Mapped[Optional[int]] = mapped_column(Integer)
    current_request_order: Mapped[Optional[int]] = mapped_column(Integer)
    supervisor_approved: Mapped[Optional[bool]] = mapped_column(Boolean)
    additional_comments: Mapped[Optional[str]] = mapped_column(Text)
    mentions_json: Mapped[Optional[str]] = mapped_column(Text)
    mentioned_user_ids: Mapped[Optional[list[int]]] = mapped_column(ARRAY(Integer()))
    advance_payment_rejected: Mapped[Optional[bool]] = mapped_column(Boolean)
    report_support_document: Mapped[Optional[str]] = mapped_column(Text)
    report_support_path: Mapped[Optional[str]] = mapped_column(Text)
    region_id: Mapped[Optional[int]] = mapped_column(Integer)
    invoice_reconciliation_required: Mapped[Optional[bool]] = mapped_column(Boolean)
    program_id: Mapped[Optional[int]] = mapped_column(Integer)
    advance_amount: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))
    rubro_id: Mapped[Optional[int]] = mapped_column(Integer)
    short_rubro: Mapped[Optional[str]] = mapped_column(Text)
    year_rubro: Mapped[Optional[int]] = mapped_column(Integer)
    activity_id: Mapped[Optional[int]] = mapped_column(Integer)
    emergency_contact: Mapped[Optional[str]] = mapped_column(Text)
    emergency_phone: Mapped[Optional[str]] = mapped_column(Text)
    emergency_relationship: Mapped[Optional[str]] = mapped_column(Text)
    

    user: Mapped[Optional[Users]] = relationship('Users')
    travel_status: Mapped[Optional['TravelStatus']] = relationship('TravelStatus')
    activity: Mapped[Optional['Activities']] = relationship('Activities')
    rubro: Mapped[Optional['Rubros']] = relationship('Rubros')
    program: Mapped[Optional['Programs']] = relationship('Programs')
    # travel_accommodations: Mapped[list['TravelAccommodations']] = relationship('TravelAccommodations', back_populates='travel_request')
    # travel_itineraries: Mapped[list['TravelItineraries']] = relationship('TravelItineraries', back_populates='travel_request')
