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
    Numeric,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
    ForeignKey,
    Uuid,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP


from entity.approval_categories import ApprovalCategory
from entity.pads import Pads
from entity.capacity_assessments import CapacityAssessments

class Pids(Base):
    __tablename__ = "pids"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pid_id_pkey"),
        UniqueConstraint("name", name="pid_name_unique"),
        ForeignKeyConstraint(["pad_id"], ["pads.id"], name="pads_pids_fkey"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(CITEXT, nullable=False)
    description: Mapped[str] = mapped_column(CITEXT, nullable=False)
    color: Mapped[str] = mapped_column(String(255), nullable=False)

    eur_usd_rate: Mapped[float] = mapped_column(Numeric, nullable=True)
    pad_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("pads.id"), nullable=True)
    usd_cop_rate: Mapped[float] = mapped_column(Numeric, nullable=True)
    eur_cop_rate: Mapped[float] = mapped_column(Numeric, nullable=True)
    sicof_code: Mapped[str] = mapped_column(String(255), nullable=True)

    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

    # RELACIONES
    pad: Mapped["Pads"] = relationship("Pads", back_populates="pids")
    
    class Config:
        from_attributes = True

 #relacion simple
    capacity_assessments_pid:  Mapped[list["CapacityAssessments"]] = relationship("CapacityAssessments", back_populates="pid") #este nombre debe coincidir con el del otro lado

    