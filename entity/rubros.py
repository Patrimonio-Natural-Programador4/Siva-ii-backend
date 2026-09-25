
from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, BigInteger, Index, PrimaryKeyConstraint, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class Rubros(Base):
    __tablename__ = 'rubros'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='rubros_pkey'),
        UniqueConstraint('rubros', name='rubros_rubros_unique'),
        Index('rubro_codigo', 'rubros', unique=True)
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    rubros: Mapped[str] = mapped_column(String(23), nullable=False)
    # created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    # updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    json_rubros: Mapped[Optional[dict]] = mapped_column(JSON, comment='Estructura JSON de rubros por año en formato: {"rubros": {"2025": "", "2024": "456", "2023": "1163"}}')
    source: Mapped[Optional[str]] = mapped_column(String(50))
    update_hws: Mapped[Optional[str]] = mapped_column(String(255))

#     acquisitions: Mapped[list['Acquisitions']] = relationship('Acquisitions', back_populates='rubro')
#     audit_acquisitions: Mapped[list['AuditAcquisitions']] = relationship('AuditAcquisitions', back_populates='rubro')
#     availabilities: Mapped[list['Availabilities']] = relationship('Availabilities', back_populates='rubro_')
#     commitments: Mapped[list['Commitments']] = relationship('Commitments', back_populates='rubro_')
#     hws: Mapped[list['Hws']] = relationship('Hws', back_populates='rubro_')
#     payment_orders: Mapped[list['PaymentOrders']] = relationship('PaymentOrders', back_populates='rubro_')
#     upt_acquisitions: Mapped[list['UptAcquisitions']] = relationship('UptAcquisitions', back_populates='rubro')
#     travel_requests: Mapped[list['TravelRequests']] = relationship('TravelRequests', back_populates='rubro')
