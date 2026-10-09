import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    BigInteger, Boolean, Date, Float, ForeignKeyConstraint, Index, Integer,
    Numeric, PrimaryKeyConstraint, Text,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base

if TYPE_CHECKING:
    
    from entity.programs import Programs
    from entity.contract_types import ContractTypes
    from entity.pillars import Pillars
    from entity.expense_categories import ExpenseCategories
    from entity.purchase_types import PurchaseTypes


class Contracts(Base):
    __tablename__ = 'contracts'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='contracts_pkey'),
        Index("code_index_contracts", "code"),
        # Foráneas
        ForeignKeyConstraint(["program_id"], ["programs.id"], name="fk_contracts_programs"),
        ForeignKeyConstraint(["contract_type_id"], ["contract_types.id"], name="fk_contracts_contract_types"),
        ForeignKeyConstraint(["pillar_id"], ["pillars.id"], name="fk_contracts_pillars"),
        ForeignKeyConstraint(["expense_category_id"], ["expense_categories.id"], name="fk_contracts_expense_categories"),
        ForeignKeyConstraint(["purchase_type_id"], ["purchase_types.id"], name="fk_contracts_purchase_types"),
        ForeignKeyConstraint(["contract_id"], ["contracts.id"], name="fk_contracts_parent"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    code: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    year: Mapped[Optional[int]] = mapped_column(Integer)
    start_contract_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    end_contract_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    subscription_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    policy_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    final_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    early_settlement_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    identification_type: Mapped[Optional[str]] = mapped_column(Text)
    identification_number: Mapped[Optional[str]] = mapped_column(Text)
    bank_code: Mapped[Optional[str]] = mapped_column(Text)
    bank_account: Mapped[Optional[str]] = mapped_column(Text)
    address_line_1: Mapped[Optional[str]] = mapped_column(Text)
    address_line_2: Mapped[Optional[str]] = mapped_column(Text)
    mobile_phone: Mapped[Optional[str]] = mapped_column(Text)

    # Foráneas
    program_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    contract_type_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    pillar_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    expense_category_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    purchase_type_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    contract_id: Mapped[Optional[int]] = mapped_column(BigInteger)          # Contrato padre (NULL = es padre)
    terms_reference_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    
    is_currency_usd: Mapped[Optional[bool]] = mapped_column(Boolean)
    policy_approval: Mapped[Optional[bool]] = mapped_column(Boolean)
    observations: Mapped[Optional[str]] = mapped_column(Text)
    causes_early_termination: Mapped[Optional[str]] = mapped_column(Text)
    sharepoint_code_new: Mapped[Optional[str]] = mapped_column(Text)
    functions_and_activities: Mapped[Optional[str]] = mapped_column(Text)
    dibursement: Mapped[Optional[str]] = mapped_column(Text)                # Descripción de los pagos
    monthly_time: Mapped[Optional[float]] = mapped_column(Float)
    final_duration: Mapped[Optional[float]] = mapped_column(Float)
    value: Mapped[Optional[int]] = mapped_column(BigInteger)
    initial_value: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    final_value: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    total_adition: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    released_resource: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    last_dibursement: Mapped[Optional[int]] = mapped_column(Integer)        # Número del último desembolso
    dibursement_value: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    total_value: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    accumulated_value: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    remaining_value: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

    # Relaciones simples
    programa: Mapped["Programs"] = relationship("Programs", back_populates="contracts_programa")
    contract_type: Mapped["ContractTypes"] = relationship("ContractTypes", back_populates="contracts_contract_type")
    pillar: Mapped["Pillars"] = relationship("Pillars", back_populates="contracts_pillar")
    expense_category: Mapped["ExpenseCategories"] = relationship("ExpenseCategories", back_populates="contracts_expense_category")
    purchase_type: Mapped["PurchaseTypes"] = relationship("PurchaseTypes", back_populates="contracts_purchase_type")

   
    parent_contract: Mapped[Optional["Contracts"]] = relationship("Contracts", remote_side="Contracts.id", back_populates="child_contracts")
    child_contracts: Mapped[list["Contracts"]] = relationship("Contracts", back_populates="parent_contract")
    
    