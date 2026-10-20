import datetime
from typing import Optional

from sqlalchemy import BigInteger, Index, text, Uuid,Boolean, Date, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP
import uuid
import decimal
from entity.disbursement import Disbursement

class DisbursementProducts(Base):
    __tablename__ = 'disbursement_products'
    __table_args__ = (
        ForeignKeyConstraint(['disbursement_id'], ['disbursement.id'], name='fk_disbursement'),
        ForeignKeyConstraint(['product_id'], ['agreements_products.id'], name='fk_disbursement_product'),
        PrimaryKeyConstraint('id', name='disbursement_products_pkey')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    disbursement_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    product_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    disbursement: Mapped['Disbursement'] = relationship('Disbursement')
    # product: Mapped['AgreementsProducts'] = relationship('AgreementsProducts', back_populates='disbursement_products')
