import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Text, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

if TYPE_CHECKING:
    from entity.users import Users

class ModelHasRoles(Base):
    __tablename__ = 'model_has_roles'
    __table_args__ = (
        ForeignKeyConstraint(['model_id'], ['users.id'], name='model_has_roles_model_id_fkey'),
        ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE', name='model_has_roles_role_id_foreign'),
        PrimaryKeyConstraint('role_id', 'model_id', 'model_type', name='model_has_roles_pkey'),
        Index('model_has_roles_model_id_model_type_index', 'model_id', 'model_type')
    )

    role_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    model_type: Mapped[str] = mapped_column(String(255), primary_key=True)
    model_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    usr: Mapped["Users"] = relationship("Users", back_populates="roles", lazy='joined')

    # model: Mapped['Users'] = relationship('Users', back_populates='model_has_roles')
    # role: Mapped['Roles'] = relationship('Roles', back_populates='model_has_roles')