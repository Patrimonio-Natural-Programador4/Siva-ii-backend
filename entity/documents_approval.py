import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base
import uuid

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    CheckConstraint,
    Text,
    ForeignKeyConstraint,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP


from entity.approval_categories import ApprovalCategory
from entity.programs import Programs


class DocumentsApproval(Base):
    __tablename__ = "documents_approval"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="documents_approval_pkey"),
        UniqueConstraint("name", name="documents_approval_name_unique"),
        ForeignKeyConstraint(
            ["approval_category_id"],
            ["approval_categories.category_id"],
            name="approval_category_id_documents_approval_fkey",
        ),
        ForeignKeyConstraint(
            ["program_id"], ["programs.id"], name="programs_documents_approval_fkey"
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    approval_category_id: Mapped[int] = mapped_column(Integer, nullable=False)
    program_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(CITEXT, nullable=False)

    # RELACIONES
    programs: Mapped["Programs"] = relationship(
        "Programs", back_populates="documents_approval"
    )
    categorias_aprobacion: Mapped["ApprovalCategory"] = relationship(
        "ApprovalCategory", back_populates="documents_approval"
    )
