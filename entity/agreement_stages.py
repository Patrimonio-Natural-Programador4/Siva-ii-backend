import datetime
from typing import Optional

from sqlalchemy import BigInteger, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP
import decimal

class AgreementStages(Base):
    __tablename__ = 'agreement_stages'
    __table_args__ = (
        ForeignKeyConstraint(['stages_id'], ['agreement_stages.id'], name='agreement_stages_id_foreign'),
        PrimaryKeyConstraint('id', name='agreement_stages')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(CITEXT)
    description: Mapped[Optional[str]] = mapped_column(CITEXT)
    color: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'gray'::character varying"))
    stages_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    stage: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    order_colum: Mapped[Optional[int]] = mapped_column(Integer)



    stage_parent: Mapped[Optional['AgreementStages']] = relationship('AgreementStages', remote_side=[id])

