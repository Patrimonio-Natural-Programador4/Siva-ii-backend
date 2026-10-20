import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, Date, ForeignKeyConstraint, Index, Integer, Numeric, PrimaryKeyConstraint, Text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


class Disbursement(Base):
    __tablename__ = 'disbursement'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='disbursement_pkey'),
        # foraneas
        ForeignKeyConstraint(['state_id'], ['disbursement_state.id'], name='fk_disbursement_state'),
        ForeignKeyConstraint(['agreement_id'], ['agreements.id'], name='fk_agreements_products_agreements'),
        ForeignKeyConstraint(['previous_studies_id'], ['previous_studies.id'], name='fk_disbursement_previous_studies'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(timezone=False))
    value: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    scheduled_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    request_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    validation_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    approval_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    disbursement_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    number_disbursement: Mapped[Optional[int]] = mapped_column(Integer)
    documento_soporte: Mapped[Optional[str]] = mapped_column(Text)
    observations: Mapped[Optional[str]] = mapped_column(Text)
    state_id: Mapped[Optional[int]] = mapped_column(BigInteger) # foranea
    agreement_id: Mapped[Optional[int]] = mapped_column(BigInteger)# foranea
    previous_studies_id: Mapped[Optional[int]] = mapped_column(BigInteger)# foranea

    # RELACIONES
    disbursement_state: Mapped[Optional["DisbursementState"]] = relationship("DisbursementState", back_populates="disbursements")
    agreement: Mapped[Optional["Agreements"]] = relationship("Agreements", back_populates="disbursements")
    previous_study: Mapped[Optional["PreviousStudies"]] = relationship("PreviousStudies", back_populates="disbursements")