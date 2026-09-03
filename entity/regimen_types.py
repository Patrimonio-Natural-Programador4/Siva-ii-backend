from __future__ import annotations
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped
from database.database import Base

class RegimenType(Base):
    __tablename__ = 'regimen_types'
    __table_args__ = {'info': {'managed_by_alembic': True}}
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
