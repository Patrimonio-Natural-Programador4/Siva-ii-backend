import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, Date, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, String, Text, Time
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


class AgreementsProducts(Base):
    __tablename__ = 'agreements_products'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='agreements_products_pkey'),
        # foraneas
        ForeignKeyConstraint(['id_agreement'], ['agreements.id'], name='agreements_products_id_agreement_foreign'),
        ForeignKeyConstraint(['state_id'], ['products_state.id'], name='agreements_products_state_id_foreign'),
        ForeignKeyConstraint(['id_product'], ['agreements_products.id'], name='fk_agreements_products'),
        ForeignKeyConstraint(['id_duplicate_product'], ['agreements_products.id'], name='fk_duplicate_product'),
        ForeignKeyConstraint(['previous_studies_id'], ['previous_studies.id'], name='fk_agreements_products_previous_studies'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    product: Mapped[str] = mapped_column(Text, nullable=False)
    code: Mapped[Optional[str]] = mapped_column(String)
    quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    value: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    unit_measure: Mapped[Optional[str]] = mapped_column(Text)
    shared_ei_one_drive: Mapped[Optional[str]] = mapped_column(Text)
    observations: Mapped[Optional[str]] = mapped_column(Text)
    expected_fulfillment_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    delivery_date: Mapped[Optional[datetime.time]] = mapped_column(Time)
    request_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    validation_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    approval_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(timezone=False))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(timezone=False))
    id_agreement: Mapped[int] = mapped_column(BigInteger, nullable=False)  # foranea
    state_id: Mapped[Optional[int]] = mapped_column(Integer)  # foranea
    id_product: Mapped[Optional[int]] = mapped_column(BigInteger)  # foranea
    id_duplicate_product: Mapped[Optional[int]] = mapped_column(BigInteger)  # foranea
    previous_studies_id: Mapped[Optional[int]] = mapped_column(BigInteger)  # foranea

    # RELACIONES 
    agreement: Mapped["Agreements"] = relationship("Agreements", back_populates="agreement_products")
    product_state: Mapped[Optional["ProductsState"]] = relationship("ProductsState", back_populates="agreement_products")
    previous_study: Mapped[Optional["PreviousStudies"]] = relationship("PreviousStudies", back_populates="agreement_products")

   
    parent_product: Mapped[Optional["AgreementsProducts"]] = relationship(
        "AgreementsProducts", remote_side=[id], foreign_keys=[id_product], back_populates="child_products"
    )
    child_products: Mapped[list["AgreementsProducts"]] = relationship(
        "AgreementsProducts", foreign_keys=[id_product], back_populates="parent_product"
    )

    # RELACIONES 
    duplicate_product: Mapped[Optional["AgreementsProducts"]] = relationship(
        "AgreementsProducts", remote_side=[id], foreign_keys=[id_duplicate_product], back_populates="duplicates"
    )
    duplicates: Mapped[list["AgreementsProducts"]] = relationship(
        "AgreementsProducts", foreign_keys=[id_duplicate_product], back_populates="duplicate_product"
    )