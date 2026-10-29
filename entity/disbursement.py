import datetime
import decimal
from typing import Optional

from sqlalchemy import BigInteger, Date, ForeignKeyConstraint, Index, Integer, Numeric, PrimaryKeyConstraint, Text, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base



class Disbursement(Base):
    __tablename__ = 'disbursement'
    __table_args__ = (
        ForeignKeyConstraint(['agreement_id'], ['agreements.id'], name='fk_agreements_products_agreements'),
        ForeignKeyConstraint(['previous_studies_id'], ['previous_studies.id'], name='fk_disbursement_previous_studies'),
        ForeignKeyConstraint(['state_id'], ['disbursement_state.id'], name='fk_disbursement_state'),
        PrimaryKeyConstraint('id', name='disbursement_pkey')
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
    agreement_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    previous_studies_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    agreement: Mapped[Optional['Agreements']] = relationship('Agreements', back_populates='disbursement')
#     previous_studies: Mapped[Optional['PreviousStudies']] = relationship('PreviousStudies', back_populates='disbursement')
    state: Mapped[Optional['DisbursementState']] = relationship('DisbursementState')
#     disbursement_products: Mapped[list['DisbursementProducts']] = relationship('DisbursementProducts', back_populates='disbursement')