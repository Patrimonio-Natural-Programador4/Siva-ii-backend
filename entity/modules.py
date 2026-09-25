
import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Text, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP


class Modules(Base):
    __tablename__ = 'modules'
    __table_args__ = (
        CheckConstraint("type::text = ANY (ARRAY['navigation'::character varying::text, 'administration'::character varying::text, 'utils'::character varying::text])", name='modules_type_check'),
        ForeignKeyConstraint(['module_id'], ['modules.id'], name='modules_module_id_foreign'),
        PrimaryKeyConstraint('id', name='modules_pkey')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(CITEXT, nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    type: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'link'::character varying"))
    order: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('10'))
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    module_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    description: Mapped[Optional[str]] = mapped_column(CITEXT)
    route: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    roles: Mapped[Optional[dict]] = mapped_column(JSON)
    permisos: Mapped[Optional[dict]] = mapped_column(JSON)

    # module: Mapped[Optional['Modules']] = relationship('Modules', remote_side=[id], back_populates='module_reverse')
    # module_reverse: Mapped[list['Modules']] = relationship('Modules', remote_side=[module_id], back_populates='module')
    # controles: Mapped[list['Controles']] = relationship('Controles', back_populates='modules')