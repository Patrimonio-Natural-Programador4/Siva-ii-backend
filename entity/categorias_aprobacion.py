from typing import Optional
from sqlalchemy import Integer, PrimaryKeyConstraint, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base

class CategoriasAprobacion(Base):
    __tablename__ = 'categorias_aprobacion'
    __table_args__ = (
        PrimaryKeyConstraint('id_categoria', name='categorias_aprobacion_pkey'),
    )

    id_categoria: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(Text)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    codigo: Mapped[Optional[str]] = mapped_column(Text)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean)
