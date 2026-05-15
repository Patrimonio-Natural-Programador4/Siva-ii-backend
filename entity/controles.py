from typing import Optional
from sqlalchemy import Boolean, Integer, Text, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base


class Controles(Base):
    __tablename__ = 'controles'
    __table_args__ = (
        ForeignKeyConstraint(['id_modulo'], ['modules.id'], name='fk_control_module'),
        PrimaryKeyConstraint('id_control', name='controles_pkey')
    )

    id_control: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[str] = mapped_column(Text, nullable=False)
    id_modulo: Mapped[int] = mapped_column(Integer, nullable=False)
    requiere_validacion: Mapped[Optional[bool]] = mapped_column(Boolean)
