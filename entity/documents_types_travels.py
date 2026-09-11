from __future__ import annotations
from typing import Optional
from sqlalchemy import Integer, String, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base


class DocumentsTypesTravels(Base):
    __tablename__ = 'documents_types_travels'
    __table_args__ = (
        PrimaryKeyConstraint('document_type_id', name='documents_types_travels_pkey'),
    )

    document_type_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    document_category: Mapped[str] = mapped_column(String(100))
