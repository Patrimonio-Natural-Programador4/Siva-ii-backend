import datetime
import uuid
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 

from sqlalchemy import BigInteger, Boolean, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text,Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

from entity.document_types import DocumentTypes
#from entity.implementer_types import Implementer_types

class Persons(Base):
    __tablename__ = "persons"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="persons_pkey"),
        #UniqueConstraint("acronym", name="acronym_unique"),
        Index("email_index", "email"),
        Index("phone_index", "phone"),
        #foranea
        ForeignKeyConstraint(
            ["identification_type"], #campo persons
            ["document_types.id"],
            name="persons_fkey",
        )
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=False)
    other_name: Mapped[str] = mapped_column(String(150), nullable=False)
    last_name: Mapped[str] = mapped_column(String(150), nullable=False)
    other_last_name: Mapped[str] = mapped_column(String(150), nullable=False)
    position: Mapped[str] = mapped_column(String(500), nullable=False)
    identification_type: Mapped[int] = mapped_column(Integer, nullable=False)
    identification_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    identification_dv: Mapped[int] = mapped_column(Integer, nullable=False)
    former_number: Mapped[int] = mapped_column(Integer,nullable=False)
    former_organization_number: Mapped[int] = mapped_column(Integer, nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    start_contract_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    end_contract_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    bank_code: Mapped[int] = mapped_column(Integer,nullable=False)
    bank_account: Mapped[str] = mapped_column(String(255), nullable=False)
    address_line_1: Mapped[str] = mapped_column(String(255), nullable=False)
    address_line_2: Mapped[str] = mapped_column(String(255), nullable=False)
    mobile_phone: Mapped[str] = mapped_column(String(255), nullable=False)
    origin: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(255), nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    person_type: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

    # RELACIONES ORM
    document_type: Mapped["DocumentTypes"] = relationship(
        "DocumentTypes", back_populates="persons"
    )
 

    