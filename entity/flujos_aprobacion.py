from __future__ import annotations
from typing import Optional, List
from sqlalchemy import Integer, Text, ForeignKeyConstraint, PrimaryKeyConstraint, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from database.database import Base
from sqlalchemy import text
from sqlalchemy.orm import mapped_column, Mapped
from entity.categorias_aprobacion import CategoriasAprobacion
from entity.flujos_aprobacion_ruta import FlujosAprobacionRuta  # Correcto para evitar problemas de importación circular

class FlujosAprobacion(Base):
    __tablename__ = 'flujos_aprobacion'
    __table_args__ = (
        ForeignKeyConstraint(['id_categoria'], ['categorias_aprobacion.id_categoria'], name='fk_flujo_aprobacion_categoria'),
        PrimaryKeyConstraint('id_flujo_aprobacion', name='flujos_aprobacion_pkey')
    )

    id_flujo_aprobacion: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(Text)
    id_categoria: Mapped[int] = mapped_column(Integer)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    aprobacion_con_anticipo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    aprobacion_legalizacion_supervisor: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    aprobacion_pagos: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    
    # Relación con CategoriasAprobacion usando el nombre de la clase como cadena
    categoria: Mapped[Optional[CategoriasAprobacion]] = relationship('CategoriasAprobacion', backref='flujos_aprobacion', lazy='joined')
    rutas: Mapped[List["FlujosAprobacionRuta"]] = relationship(
        "FlujosAprobacionRuta",
        back_populates="flujos_aprobacion",
        cascade="all, delete-orphan"
    )
    # Si necesitas otras relaciones, puedes descomentarlas
    # flujos_aprobacion_ruta: Mapped[List[FlujosAprobacionRuta]] = relationship('FlujosAprobacionRuta', back_populates='flujos_aprobacion')
    # solicitudes_aprobacion: Mapped[List['SolicitudesAprobacion']] = relationship('SolicitudesAprobacion', back_populates='flujos_aprobacion')
