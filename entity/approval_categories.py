from typing import Optional
from sqlalchemy import Integer, PrimaryKeyConstraint, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base

class ApprovalCategory(Base):
    __tablename__ = 'approval_categories'

    __table_args__ = (
        PrimaryKeyConstraint(
            'category_id',
            name='approval_categories_pkey'
        ),
    )

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    code: Mapped[Optional[str]] = mapped_column(Text)
    active: Mapped[Optional[bool]] = mapped_column(Boolean)