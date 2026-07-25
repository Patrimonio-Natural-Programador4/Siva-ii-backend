from typing import Optional
from sqlalchemy import Boolean, Integer, Text, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from database.database import Base

class ExpenseAdvanceConcepts(Base):
    __tablename__ = 'expense_advance_concepts'
    __table_args__ = (
        PrimaryKeyConstraint('expense_advance_concept_id', name='advance_concepts_pkey'),
    )

    expense_advance_concept_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    concept: Mapped[str] = mapped_column(Text, nullable=False)