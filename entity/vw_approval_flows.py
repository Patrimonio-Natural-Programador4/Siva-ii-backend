from __future__ import annotations
from typing import Optional, List
from sqlalchemy import ARRAY, Integer, Text, ForeignKeyConstraint, PrimaryKeyConstraint, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from database.database import Base
from sqlalchemy import text
from sqlalchemy.orm import mapped_column, Mapped

from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class VWApprovalFlows(Base):
    __tablename__ = 'vw_approval_flows'

    # Definición manual de las columnas de la vista
    unique_id = Column(Integer, primary_key=True)
    approval_flow_id = Column(Integer)  # Si tiene una columna primaria, la dejamos aquí
    name = Column(Text)
    description = Column(Text)
    category_id = Column(Integer)
    category = Column(Text)
    flow_active = Column(Boolean)
    category_code = Column(Text)
    step_id = Column(Integer)
    approval_role_id = Column(Integer)
    step_order = Column(Integer)
    step_active = Column(Boolean)
    approval_role = Column(Text)
    role_active = Column(Boolean)
    user_id = Column(Integer)
    user_role_active = Column(Boolean)
    assign_travel_budget = Column(Boolean)
    adjust_travel_itinerary = Column(Boolean)
    validate_supporting_documents = Column(Boolean)
    validate_hotel_documents = Column(Boolean)
    disable_advance_concepts = Column(Boolean)
    add_rpc = Column(Boolean)
    add_accounting_document = Column(Boolean)
    is_supervisor = Column(Boolean)
    add_medical_assistance_card = Column(Boolean)
    add_expense_voucher = Column(Boolean)
    approval_with_advance = Column(Boolean)
    #delegated_user_ids = Column(ARRAY(Integer()))
    enable_payment = Column(Boolean)
    enable_payment_rejection = Column(Boolean)
    supervisor_settlement_approval = Column(Boolean)
    payment_approval = Column(Boolean)
    program_id = Column(Integer)

    __mapper_args__ = {
        'primary_key': [unique_id]  # Usar la columna artificial como clave primaria
    }

    @classmethod
    def __declare_last__(cls):
        pass  # Este método podría usarse para evitar operaciones de escritura adicionales

