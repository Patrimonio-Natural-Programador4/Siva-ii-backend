
import uuid

from alembic.environment import Optional
import datetime
from sqlalchemy import Text, DateTime, text
from sqlalchemy import Integer, PrimaryKeyConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class TermsReference(Base):
    __tablename__ = 'terms_reference'
    __table_args__ = (
        PrimaryKeyConstraint('terms_reference_id', name='terms_reference_pkey'),
    )

    terms_reference_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rubro_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pid_id: Mapped[int] = mapped_column(Integer, nullable=False)
    expense_categories_id: Mapped[int] = mapped_column(Integer, nullable=False)
    selection_procedure_id: Mapped[int] = mapped_column(Integer, nullable=False)
    activity_id: Mapped[int] = mapped_column(Integer, nullable=False)
    evaluation_method_id: Mapped[int] = mapped_column(Integer, nullable=False)
    guid: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    object: Mapped[Optional[str]] = mapped_column(Text)
    process_number: Mapped[Optional[str]] = mapped_column(Text)
    scope: Mapped[Optional[str]] = mapped_column(Text)
    execution_period: Mapped[Optional[str]] = mapped_column(Text)
    place_execution: Mapped[Optional[str]] = mapped_column(Text)
    supervisor_id: Mapped[Optional[int]] = mapped_column(Integer)
    educational_background: Mapped[Optional[str]] = mapped_column(Text)
    general_professional_experience: Mapped[Optional[str]] = mapped_column(Text)
    name: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    program_id: Mapped[Optional[int]] = mapped_column(Integer)
    approval_request_id: Mapped[Optional[int]] = mapped_column(Integer)
    created_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    status_id: Mapped[Optional[int]] = mapped_column(Integer)