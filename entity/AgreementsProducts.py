import datetime
from typing import Optional

from sqlalchemy import BigInteger, Index, text, Uuid,Boolean, Date, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP
import uuid
import decimal

class AgreementsProducts(Base):
    __tablename__ = 'agreements_products'
    __table_args__ = (
        ForeignKeyConstraint(['id_agreement'], ['agreements.id'], name='agreements_products_id_agreement_foreign'),
        ForeignKeyConstraint(['id_duplicate_product'], ['agreements_products.id'], ondelete='SET NULL', name='fk_duplicate_product'),
        ForeignKeyConstraint(['id_product'], ['agreements_products.id'], name='fk_agreements_products'),
        ForeignKeyConstraint(['state_id'], ['products_state.id'], name='agreements_products_state_id_foreign'),
        PrimaryKeyConstraint('id', name='agreements_products_pkey'),
        Index('idx_duplicate_product', 'id_duplicate_product')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    id_agreement: Mapped[int] = mapped_column(BigInteger, nullable=False)
    product: Mapped[str] = mapped_column(Text, nullable=False)
    id_product: Mapped[Optional[int]] = mapped_column(BigInteger)
    code: Mapped[Optional[str]] = mapped_column(String(255))
    quantity: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(15, 2))
    value: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(15, 2))
    unit_measure: Mapped[Optional[str]] = mapped_column(Text)
    expected_fulfillment_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    # delivery_date: Mapped[Optional[datetime.time]] = mapped_column(TIME(precision=0))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    shared_ei_one_drive: Mapped[Optional[str]] = mapped_column(Text)
    observations: Mapped[Optional[str]] = mapped_column(Text)
    request_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    validation_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    state_id: Mapped[Optional[int]] = mapped_column(Integer)
    approval_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    id_duplicate_product: Mapped[Optional[int]] = mapped_column(BigInteger)

    # agreements: Mapped['Agreements'] = relationship('Agreements', back_populates='agreements_products')
    # agreements_products: Mapped[Optional['AgreementsProducts']] = relationship('AgreementsProducts', remote_side=[id], foreign_keys=[id_duplicate_product], back_populates='agreements_products_reverse')
    # agreements_products_reverse: Mapped[list['AgreementsProducts']] = relationship('AgreementsProducts', remote_side=[id_duplicate_product], foreign_keys=[id_duplicate_product], back_populates='agreements_products')
    # agreements_products: Mapped[Optional['AgreementsProducts']] = relationship('AgreementsProducts', remote_side=[id], foreign_keys=[id_product])
    # agreements_products__reverse: Mapped[list['AgreementsProducts']] = relationship('AgreementsProducts', remote_side=[id_product], foreign_keys=[id_product], back_populates='agreements_products_')
    # state: Mapped[Optional['ProductsState']] = relationship('ProductsState', back_populates='agreements_products')
    # disbursement_products: Mapped[list['DisbursementProducts']] = relationship('DisbursementProducts', back_populates='product')
