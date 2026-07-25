import datetime
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
import uuid

from sqlalchemy import BigInteger, Boolean, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, String, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        # ForeignKeyConstraint(['identification_type'], ['document_types.id'], name='users_identification_type_foreign'),
        # ForeignKeyConstraint(['person_id'], ['persons.id'], name='users_person_id_foreign'),
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_unique'),
        UniqueConstraint('identification_number', name='users_identification_number_unique'),
        UniqueConstraint('person_id', name='users_person_id_unique'),
        Index('users_email_index', 'email'),
        Index('users_identification_number_index', 'identification_number')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(CITEXT, nullable=False)
    last_name: Mapped[str] = mapped_column(CITEXT, nullable=False)
    identification_type: Mapped[int] = mapped_column(BigInteger, nullable=False)
    identification_number: Mapped[int] = mapped_column(BigInteger, nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    guid: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, server_default=text('gen_random_uuid()'))
    other_name: Mapped[Optional[str]] = mapped_column(CITEXT)
    other_last_name: Mapped[Optional[str]] = mapped_column(CITEXT)
    position: Mapped[Optional[str]] = mapped_column(CITEXT)
    email_verified_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    mobile_phone: Mapped[Optional[str]] = mapped_column(String(255))
    remember_token: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    person_id: Mapped[Optional[int]] = mapped_column(Integer)
    guid_msft: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    full_name: Mapped[Optional[str]] = mapped_column(CITEXT)
    # document_types: Mapped['DocumentTypes'] = relationship('DocumentTypes', back_populates='users')
    # person: Mapped[Optional['Persons']] = relationship('Persons', back_populates='users')
    # annotations: Mapped[list['Annotations']] = relationship('Annotations', back_populates='user')
    # notifications: Mapped[list['Notifications']] = relationship('Notifications', back_populates='user')
    # tasks_applicant: Mapped[list['Tasks']] = relationship('Tasks', foreign_keys='[Tasks.applicant_id]', back_populates='applicant')
    # tasks_executor: Mapped[list['Tasks']] = relationship('Tasks', foreign_keys='[Tasks.executor_id]', back_populates='executor')
    # tasks_responsible: Mapped[list['Tasks']] = relationship('Tasks', foreign_keys='[Tasks.responsible_id]', back_populates='responsible')
    # tasks_reviewer: Mapped[list['Tasks']] = relationship('Tasks', foreign_keys='[Tasks.reviewer_id]', back_populates='reviewer')
    # observations: Mapped[list['Observations']] = relationship('Observations', back_populates='users')