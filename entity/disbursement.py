import datetime
from typing import Optional

from sqlalchemy import BigInteger, Index, text, Uuid,Boolean, Date, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP
import uuid
import decimal

class Disbursement(Base):
    __tablename__ = 'disbursement'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='disbursement_pkey'),
        # ForeignKeyConstraint(['state_id'], ['disbursement_state.id'], name='fk_disbursement_state'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(True, 0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    value: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(15, 2))
    scheduled_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    request_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    validation_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    approval_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    number_disbursement: Mapped[Optional[int]] = mapped_column(Integer)
    disbursement_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    state_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    documento_soporte: Mapped[Optional[str]] = mapped_column(Text)
    observations: Mapped[Optional[str]] = mapped_column(Text)

    # state: Mapped[Optional['DisbursementState']] = relationship('DisbursementState', back_populates='disbursement')
    # disbursement_products: Mapped[list['DisbursementProducts']] = relationship('DisbursementProducts', back_populates='disbursement')
