from typing import Optional
from sqlalchemy import Boolean, Integer, Text, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from database.database import Base

class AccountTypes(Base):
    __tablename__ = 'account_types'
    __table_args__ = (
        PrimaryKeyConstraint('account_type_id', name='account_types_pkey'),
    )

    account_type_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_type: Mapped[str] = mapped_column(Text, nullable=False)
