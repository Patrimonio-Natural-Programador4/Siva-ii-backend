from typing import Optional
from sqlalchemy import Boolean, Integer, Text, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from database.database import Base


class Banks(Base):
    __tablename__ = 'banks'
    __table_args__ = (
        PrimaryKeyConstraint('bank_id', name='banks_pkey'),
    )

    bank_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bank: Mapped[str] = mapped_column(Text, nullable=False)