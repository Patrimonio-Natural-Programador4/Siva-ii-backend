from __future__ import annotations
from typing import Optional, List, Any
from sqlalchemy import Integer, Date, Text, ForeignKeyConstraint, PrimaryKeyConstraint, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from database.database import Base
from sqlalchemy import Sequence, text
from sqlalchemy.orm import mapped_column, Mapped
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entity.roles_aprobacion_usuarios import RolesAprobacionUsuarios
    from entity.flujos_aprobacion_ruta import FlujosAprobacionRuta

class RolesAprobacion(Base):
    __tablename__ = 'roles_aprobacion'
    __table_args__ = (
        PrimaryKeyConstraint('id_rol_aprobacion', name='roles_aprobacion_pkey'),
    )

    id_rol_aprobacion: Mapped[int] = mapped_column(Integer, Sequence('roles_aprobacion_id_rol_seq'), primary_key=True)
    nombre: Mapped[str] = mapped_column(Text)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    es_supervisor: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    # flujos_aprobacion_ruta: Mapped[List['FlujosAprobacionRuta']] = relationship('FlujosAprobacionRuta', back_populates='roles_aprobacion')
    roles_usuarios: Mapped[List["RolesAprobacionUsuarios"]] = relationship(
        "RolesAprobacionUsuarios",
        back_populates="rol_aprobacion",
        cascade="all, delete-orphan"
    )
    rechaza_pagos: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    ruta: Mapped["FlujosAprobacionRuta"] = relationship("FlujosAprobacionRuta", back_populates="rol")
    # solicitudes_aprobacion_historial: Mapped[List['SolicitudesAprobacionHistorial']] = relationship('SolicitudesAprobacionHistorial', back_populates='roles_aprobacion')
