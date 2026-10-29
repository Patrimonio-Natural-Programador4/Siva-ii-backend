import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import declarative_base
from database.database import Base 
from sqlalchemy import Column, Text

from sqlalchemy import BigInteger, ForeignKeyConstraint, Index, Integer, Numeric, PrimaryKeyConstraint, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP

from entity.activities import Activities
from entity.agreements import Agreements
from entity.codes import Codes
from entity.contracts import Contracts
from entity.expense_categories import ExpenseCategories
from entity.pads import Pads
from entity.Pidss import Pids
from entity.purchase_types import PurchaseTypes


class Acquisitions(Base):
    __tablename__ = 'acquisitions'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='acquisitions_pkey'),
        #foranea
        ForeignKeyConstraint
        (
            ["activity_id"], 
            ["activities.id"],
            name="acquisitions_activity_id_foreign",
        ),
        ForeignKeyConstraint(["agreement_id"], ["agreements.id"],name="acquisitions_agreement_id_foreign"),
        ForeignKeyConstraint(["code_id"], ["codes.id"],name="acquisitions_code_id_foreign"),
        ForeignKeyConstraint(["contractt_id"], ["contracts.id"],name="acquisitions_contractt_id_foreign"),
        ForeignKeyConstraint(["expense_category_id"], ["expense_categories.id"],name="acquisitions_expense_category_id_foreign"),
        ForeignKeyConstraint(["pad_id"], ["pads.id"],name="acquisitions_pad_id_foreign"),
        ForeignKeyConstraint(["pid_id"], ["pids.id"],name="acquisitions_pid_id_foreign"),
        ForeignKeyConstraint(["purchase_type_id"], ["purchase_types.id"],name="acquisitions_purchase_type_id_foreign"),
    )

    id: Mapped[int] =                   mapped_column(BigInteger, primary_key=True)
    process_number: Mapped[int] =       mapped_column(Integer, nullable=False)
    type: Mapped[str] =                 mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    numero_contrato_temporal: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[Optional[str]] =     mapped_column(String)
    contracts_qty: Mapped[Optional[int]] = mapped_column(Integer)

    activity_id: Mapped[int] = mapped_column(BigInteger, nullable=False) 
    expense_category_id: Mapped[int] = mapped_column(BigInteger, nullable=False) 
    purchase_type_id: Mapped[int] = mapped_column(BigInteger, nullable=False) 
    agreement_id: Mapped[Optional[int]] = mapped_column(BigInteger) 
    code_id: Mapped[Optional[int]] = mapped_column(BigInteger) 
    contractt_id: Mapped[Optional[int]] = mapped_column(BigInteger) 
    pad_id: Mapped[Optional[int]] = mapped_column(BigInteger) 
    pid_id: Mapped[Optional[int]] = mapped_column(BigInteger) 

    contract_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    rubro_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    status_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    general_cat_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    kfw_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    person_id_implementer: Mapped[Optional[int]] = mapped_column(BigInteger)
    person_id_executer: Mapped[Optional[int]] = mapped_column(BigInteger)
    vlr_id_typ_hiring: Mapped[Optional[int]] = mapped_column(BigInteger)
    vlr_id_sts_hiring: Mapped[Optional[int]] = mapped_column(BigInteger)
    vlr_id_typ_gnrl_ctg: Mapped[Optional[int]] = mapped_column(BigInteger)

    trm: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    initial_budget_cop: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    initial_budget_usd: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    initial_budget_eur: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    final_budget_cop: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    final_budget_usd: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    final_budget_eur: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    appropriate: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    appropriate_pending: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    fulfilled: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    unfulfilled: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    paid_total_value: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    unpaid_total_value: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    apropiate_sicof: Mapped[Optional[int]] = mapped_column(BigInteger)
    execute_sicof: Mapped[Optional[int]] = mapped_column(BigInteger)

    acquisition_detail: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    detail: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    code: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    code_siva: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    observations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cod_siva_contrato: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    cod_siva_acuerdo: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    version_creation: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    version_update: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

    #Relaciones
    activity: Mapped["Activities"] = relationship("Activities", back_populates="acquisitions_activity")
    agreement: Mapped["Agreements"] = relationship("Agreements", back_populates="acquisitions_agreement")
    code_rel: Mapped["Codes"] = relationship("Codes", back_populates="acquisitions_code")
    contractt: Mapped["Contracts"] = relationship("Contracts", back_populates="acquisitions_contractt")
    expense_category: Mapped["ExpenseCategories"] = relationship("ExpenseCategories", back_populates="acquisitions_expense_category")
    pad: Mapped["Pads"] = relationship("Pads", back_populates="acquisitions_pad")
    pid: Mapped["Pids"] = relationship("Pids", back_populates="acquisitions_pid")
    purchase_type: Mapped["PurchaseTypes"] = relationship("PurchaseTypes", back_populates="acquisitions_purchase_type")