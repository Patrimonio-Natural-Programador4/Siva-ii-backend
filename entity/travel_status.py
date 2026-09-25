from typing import Optional
from sqlalchemy import Boolean, Integer, Text, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from database.database import Base

class TravelStatus(Base):
    __tablename__ = 'travel_status'
    __table_args__ = (
        PrimaryKeyConstraint('status_id', name='travel_status_pkey'),
    )

    status_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(Text)

    # travel_requests: Mapped[list['TravelRequests']] = relationship('TravelRequests', back_populates='travel_status')
