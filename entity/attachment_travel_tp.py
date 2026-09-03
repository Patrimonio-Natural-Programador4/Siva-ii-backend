from __future__ import annotations
from typing import Optional
from sqlalchemy import Integer, Text, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base


class AttachmentTravelTp(Base):
    __tablename__ = 'attachment_travel_tp'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='attachment_travel_tp_pkey'),
        ForeignKeyConstraint(
            ['travel_request_id'],
            ['travel_requests.travel_request_id'],
            name='fk_attachment_travel_tp_travel_request',
            ondelete='CASCADE'
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    attachment_name: Mapped[Optional[str]] = mapped_column(Text)
    path_document: Mapped[Optional[str]] = mapped_column(Text)
    travel_request_id: Mapped[Optional[int]] = mapped_column(Integer)
