from __future__ import annotations
from typing import Optional
from sqlalchemy import Integer, Text, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base


class AttachmentExcel(Base):
    __tablename__ = 'attachment_excel'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='attachment_excel_pkey'),
        ForeignKeyConstraint(
            ['travel_request_id'],
            ['travel_requests.travel_request_id'],
            name='fk_attachment_excel_travel_request',
            ondelete='CASCADE'
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    attachment_name: Mapped[Optional[str]] = mapped_column(Text)
    travel_request_id: Mapped[Optional[int]] = mapped_column(Integer)
