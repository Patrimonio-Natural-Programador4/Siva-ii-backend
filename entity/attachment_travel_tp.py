from __future__ import annotations
from typing import Optional
from sqlalchemy import Integer, Text, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base
from entity.documents_types_travels import DocumentsTypesTravels


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
        ForeignKeyConstraint(
            ['document_type_id'],
            ['documents_types_travels.document_type_id'],
            name='fk_attachment_travel_tp_doc_type',
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    attachment_name: Mapped[Optional[str]] = mapped_column(Text)
    path_document: Mapped[Optional[str]] = mapped_column(Text)
    travel_request_id: Mapped[Optional[int]] = mapped_column(Integer)
    observations: Mapped[Optional[str]] = mapped_column(Text)
    document_type_id: Mapped[Optional[int]] = mapped_column(Integer)
