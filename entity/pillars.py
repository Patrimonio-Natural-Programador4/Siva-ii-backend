#ENTITY ESTUDIOS PREVIOS

import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Text, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint,Date, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP


class Pillars(Base):
    __tablename__ = 'pillars'
    __table_args__ = (
        CheckConstraint("color::text = ANY (ARRAY['neutral'::character varying::text, 'lime'::character varying::text, 'blue'::character varying::text, 'gray'::character varying::text, 'red'::character varying::text, 'green'::character varying::text, 'yellow'::character varying::text, 'indigo'::character varying::text, 'purple'::character varying::text, 'pink'::character varying::text, 'slate'::character varying::text, 'orange'::character varying::text, 'amber'::character varying::text, 'teal'::character varying::text, 'sky'::character varying::text])", name='pillars_color_check'),
        PrimaryKeyConstraint('id', name='pillars_pkey'),
        UniqueConstraint('name', name='pillars_name_unique')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(CITEXT, nullable=False)
    color: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'gray'::character varying"))
    description: Mapped[Optional[str]] = mapped_column(CITEXT)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

#     activities: Mapped[list['Activities']] = relationship('Activities', back_populates='pillar')
#     agreements: Mapped[list['Agreements']] = relationship('Agreements', back_populates='pillar')
#     contracts: Mapped[list['Contracts']] = relationship('Contracts', back_populates='pillar')