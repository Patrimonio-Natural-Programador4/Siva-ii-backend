from __future__ import annotations
from typing import Optional, List, Any
from sqlalchemy import Integer, Date, Text, ForeignKeyConstraint, PrimaryKeyConstraint, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from database.database import Base
from sqlalchemy import Sequence, text
from sqlalchemy.orm import mapped_column, Mapped
from entity.roles_aprobacion import RolesAprobacion
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entity.flujos_aprobacion import FlujosAprobacion
    
class FlujosAprobacionRuta(Base):
    __tablename__ = 'flujos_aprobacion_ruta'
    __table_args__ = (
        ForeignKeyConstraint(['id_flujo_aprobacion'], ['flujos_aprobacion.id_flujo_aprobacion'], name='fk_flujo_aprobacion'),
        ForeignKeyConstraint(['id_rol_aprobacion'], ['roles_aprobacion.id_rol_aprobacion'], name='fk_flujo_aprobacion_rol'),
        PrimaryKeyConstraint('id_ruta', name='flujos_aprobacion_ruta_pkey')
    )

    id_ruta: Mapped[int] = mapped_column(Integer, Sequence('flujos_aprobacion_ruta_id_ruta_seq'), primary_key=True)
    id_flujo_aprobacion: Mapped[int] = mapped_column(Integer)
    id_rol_aprobacion: Mapped[int] = mapped_column(Integer)
    orden: Mapped[int] = mapped_column(Integer)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    copia_correos_solicitud: Mapped[Optional[str]] = mapped_column(Text)
    copia_correos_ajustes: Mapped[Optional[str]] = mapped_column(Text)
    copia_correos_aprobcion: Mapped[Optional[str]] = mapped_column(Text)

    flujos_aprobacion: Mapped['FlujosAprobacion'] = relationship('FlujosAprobacion', back_populates='rutas')
    rol: Mapped['RolesAprobacion'] = relationship('RolesAprobacion', back_populates='ruta')
    asigna_presupuesto_viajes: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    enviar_notificacion_pagos: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    habilitar_rechazar_pago: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
        
    
    # rol: Mapped[List["RolesAprobacion"]] = relationship(
    #     "RolesAprobacion",
    #     back_populates="ruta",
    #     cascade="all, delete-orphan"
    # )
