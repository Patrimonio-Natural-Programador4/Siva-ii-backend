
from sqlalchemy import BigInteger, ForeignKeyConstraint, PrimaryKeyConstraint, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
import datetime

from database.database import Base


class Activities(Base):
    __tablename__ = 'activities'
    __table_args__ = (
        ForeignKeyConstraint(['activity_id'], ['activities.id'], name='activities_activity_id_foreign'),
        ForeignKeyConstraint(['pillar_id'], ['pillars.id'], name='activities_pillar_id_foreign'),
        PrimaryKeyConstraint('id', name='activities_pkey')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    pillar_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    activity_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    description: Mapped[Optional[str]] = mapped_column(Text)
    # created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    # updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    is_logistics_expense_associate: Mapped[Optional[bool]] = mapped_column(Boolean)

#     activity: Mapped[Optional['Activities']] = relationship('Activities', remote_side=[id], back_populates='activity_reverse')
#     activity_reverse: Mapped[list['Activities']] = relationship('Activities', remote_side=[activity_id], back_populates='activity')
#     pillar: Mapped['Pillars'] = relationship('Pillars', back_populates='activities')
#     acquisitions: Mapped[list['Acquisitions']] = relationship('Acquisitions', back_populates='activity')
#     audit_acquisitions: Mapped[list['AuditAcquisitions']] = relationship('AuditAcquisitions', back_populates='activity')
#     availabilities: Mapped[list['Availabilities']] = relationship('Availabilities', back_populates='activity')
#     commitments: Mapped[list['Commitments']] = relationship('Commitments', back_populates='activity')
#     hws: Mapped[list['Hws']] = relationship('Hws', back_populates='activity')
#     lines: Mapped[list['Lines']] = relationship('Lines', back_populates='activity')
#     payment_orders: Mapped[list['PaymentOrders']] = relationship('PaymentOrders', back_populates='activity')
#     upt_acquisitions: Mapped[list['UptAcquisitions']] = relationship('UptAcquisitions', back_populates='activity')
#     travel_requests: Mapped[list['TravelRequests']] = relationship('TravelRequests', back_populates='activity')