from __future__ import annotations
from typing import Optional, List, Any
from sqlalchemy import Integer, Date, Text, ForeignKeyConstraint, PrimaryKeyConstraint, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from database.database import Base
from sqlalchemy import Sequence, text
from sqlalchemy.orm import mapped_column, Mapped
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entity.users import Users
    from entity.roles_aprobacion import RolesAprobacion

class RolesAprobacionUsuarios(Base):
    __tablename__ = 'roles_aprobacion_usuarios'
    __table_args__ = (
        ForeignKeyConstraint(['id_rol_aprobacion'], ['roles_aprobacion.id_rol_aprobacion'], name='fk_rol_aprobacion'),
        ForeignKeyConstraint(['id_usuario'], ['users.id'], name='fk_rol_aprobacion_usuario'),
        PrimaryKeyConstraint('id_rol_usuario', name='roles_aprobacion_usuarios_pkey')
    )

    id_rol_usuario: Mapped[int] = mapped_column(Integer, Sequence('rolea_aprobacion_usuarios_id_rol_usuario_seq'), primary_key=True)
    id_rol_aprobacion: Mapped[int] = mapped_column(Integer)
    id_usuario: Mapped[int] = mapped_column(Integer)
    activo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    usuario: Mapped[Optional[Users]] = relationship('Users', foreign_keys=[id_usuario], lazy='joined')
    rol_aprobacion: Mapped["RolesAprobacion"] = relationship("RolesAprobacion", back_populates="roles_usuarios")
