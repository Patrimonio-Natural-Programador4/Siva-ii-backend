import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import BigInteger, Boolean, Column, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, Table, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

t_role_has_permissions = Table(
    'role_has_permissions', Base.metadata,
    Column('permission_id', BigInteger, primary_key=True),
    Column('role_id', BigInteger, primary_key=True),
    ForeignKeyConstraint(['permission_id'], ['permissions.id'], ondelete='CASCADE', name='role_has_permissions_permission_id_foreign'),
    ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE', name='role_has_permissions_role_id_foreign'),
    PrimaryKeyConstraint('permission_id', 'role_id', name='role_has_permissions_pkey')
)
