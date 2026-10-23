from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal


class AcquisitionsBase(BaseModel):
    id: Optional[int] = None
    process_number: Optional[int] = None
    type: Optional[str] = None
    description: Optional[str] = None
    numero_contrato_temporal: Optional[str] = None
    status: Optional[str] = None
    contracts_qty: Optional[int] = None

    activity_id: Optional[int] = None
    activity_code: Optional[str] = None
    activity_description: Optional[str] = None
    expense_category_id: Optional[int] = None
    expense_category_name: Optional[str] = None
    purchase_type_id: Optional[int] = None
    purchase_type_name: Optional[str] = None
    agreement_id: Optional[int] = None
    agreement_code: Optional[str] = None
    code_id: Optional[int] = None
    contractt_id: Optional[int] = None
    contract_code: Optional[str] = None
    pad_id: Optional[int] = None
    pid_id: Optional[int] = None
    pad_name: Optional[str] = None
    contract_id: Optional[int] = None
    rubro_id: Optional[int] = None
    status_id: Optional[int] = None
    general_cat_id: Optional[int] = None
    kfw_id: Optional[int] = None
    person_id_implementer: Optional[int] = None
    person_id_executer: Optional[int] = None
    vlr_id_typ_hiring: Optional[int] = None
    vlr_id_sts_hiring: Optional[int] = None
    vlr_id_typ_gnrl_ctg: Optional[int] = None
    trm: Optional[Decimal] = None
    initial_budget_cop: Optional[Decimal] = None
    initial_budget_usd: Optional[Decimal] = None
    initial_budget_eur: Optional[Decimal] = None
    final_budget_cop: Optional[Decimal] = None
    final_budget_usd: Optional[Decimal] = None
    final_budget_eur: Optional[Decimal] = None
    appropriate: Optional[Decimal] = None
    appropriate_pending: Optional[Decimal] = None
    fulfilled: Optional[Decimal] = None
    unfulfilled: Optional[Decimal] = None
    paid_total_value: Optional[Decimal] = None
    unpaid_total_value: Optional[Decimal] = None
    apropiate_sicof: Optional[int] = None
    execute_sicof: Optional[int] = None
    acquisition_detail: Optional[str] = None
    detail: Optional[str] = None
    code: Optional[str] = None
    code_siva: Optional[str] = None
    observations: Optional[str] = None
    cod_siva_contrato: Optional[str] = None
    cod_siva_acuerdo: Optional[str] = None
    version_creation: Optional[str] = None
    version_update: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AcquisitionsCreate(BaseModel):
    process_number: Optional[int] = None
    type: Optional[str] = None
    description: Optional[str] = None
    numero_contrato_temporal: Optional[str] = None
    status: Optional[str] = None
    contracts_qty: Optional[int] = None
    activity_id: Optional[int] = None
    expense_category_id: Optional[int] = None
    purchase_type_id: Optional[int] = None
    agreement_id: Optional[int] = None
    code_id: Optional[int] = None
    contractt_id: Optional[int] = None
    pad_id: Optional[int] = None
    pid_id: Optional[int] = None
    rubro_id: Optional[int] = None
    status_id: Optional[int] = None
    general_cat_id: Optional[int] = None
    kfw_id: Optional[int] = None
    person_id_implementer: Optional[int] = None
    person_id_executer: Optional[int] = None
    trm: Optional[Decimal] = None
    initial_budget_cop: Optional[Decimal] = None
    initial_budget_usd: Optional[Decimal] = None
    initial_budget_eur: Optional[Decimal] = None
    final_budget_cop: Optional[Decimal] = None
    final_budget_usd: Optional[Decimal] = None
    final_budget_eur: Optional[Decimal] = None
    appropriate: Optional[Decimal] = None
    appropriate_pending: Optional[Decimal] = None
    fulfilled: Optional[Decimal] = None
    unfulfilled: Optional[Decimal] = None
    detail: Optional[str] = None
    code: Optional[str] = None
    code_siva: Optional[str] = None
    observations: Optional[str] = None
    cod_siva_contrato: Optional[str] = None
    cod_siva_acuerdo: Optional[str] = None

    class Config:
        from_attributes = True




class AcquisitionListSP(BaseModel):
    id: Optional[int] = None
    process_number: Optional[str] = None
    pid_id: Optional[int] = None
    pad_name: Optional[str] = None
    pillar_id: Optional[int] = None
    pillar_name: Optional[str] = None
    activity_id: Optional[int] = None
    activity_code: Optional[str] = None
    activity_description: Optional[str] = None
    code_siva: Optional[str] = None
    implementer_name: Optional[str] = None
    executer_name: Optional[str] = None
    rubro_id: Optional[int] = None
    rubro_name: Optional[str] = None
    rubro_corto: Optional[str] = None
    general_category_name: Optional[str] = None
    expense_category_name: Optional[str] = None
    purchase_type_name: Optional[str] = None
    contracts_qty: Optional[int] = None
    detail: Optional[str] = None
    code: Optional[str] = None
    agreement_id: Optional[int] = None
    cod_siva_acuerdo: Optional[str] = None
    contract_id: Optional[int] = None
    cod_siva_contrato: Optional[str] = None
    observations: Optional[str] = None
    status_id: Optional[int] = None
    status_name: Optional[str] = None
    kfw_name: Optional[str] = None
    departamento: Optional[str] = None
    municipio: Optional[str] = None
    vereda: Optional[str] = None
    policy_date: Optional[date] = None
    start_contract_date: Optional[date] = None
    finish_date: Optional[date] = None
    end_contract_date: Optional[date] = None
    final_date: Optional[date] = None
    final_date_con: Optional[date] = None
    liquidation_date: Optional[date] = None
    early_settlement_date: Optional[date] = None
    initial_budget_cop: Optional[Decimal] = None
    initial_budget_usd: Optional[Decimal] = None
    initial_budget_eur: Optional[Decimal] = None
    final_budget_cop: Optional[Decimal] = None
    final_budget_usd: Optional[Decimal] = None
    final_budget_eur: Optional[Decimal] = None
    appropriate: Optional[Decimal] = None
    appropriate_sicof: Optional[Decimal] = None
    appropriate_pending: Optional[Decimal] = None
    fulfilled: Optional[Decimal] = None
    execute_sicof: Optional[Decimal] = None
    unfulfilled: Optional[Decimal] = None
    value: Optional[Decimal] = None
    value_con: Optional[Decimal] = None
    total_final_value: Optional[Decimal] = None
    total_final_value_con: Optional[Decimal] = None
    can_delete: Optional[bool] = None
    grand_initial_budget_cop: Optional[Decimal] = None
    grand_initial_budget_usd: Optional[Decimal] = None
    grand_initial_budget_eur: Optional[Decimal] = None
    grand_final_budget_cop: Optional[Decimal] = None
    grand_final_budget_usd: Optional[Decimal] = None
    grand_final_budget_eur: Optional[Decimal] = None
    grand_appropriate: Optional[Decimal] = None
    grand_appropriate_sicof: Optional[Decimal] = None
    grand_appropriate_pending: Optional[Decimal] = None
    grand_fulfilled: Optional[Decimal] = None
    grand_execute_sicof: Optional[Decimal] = None
    grand_unfulfilled: Optional[Decimal] = None
    grand_value: Optional[Decimal] = None
    grand_value_con: Optional[Decimal] = None
    grand_total_final_value: Optional[Decimal] = None
    grand_total_final_value_con: Optional[Decimal] = None
    total_records: Optional[int] = None
    page_initial_budget_cop: Optional[Decimal] = None
    page_initial_budget_usd: Optional[Decimal] = None
    page_initial_budget_eur: Optional[Decimal] = None
    page_final_budget_cop: Optional[Decimal] = None
    page_final_budget_usd: Optional[Decimal] = None
    page_final_budget_eur: Optional[Decimal] = None
    page_appropriate: Optional[Decimal] = None
    page_appropriate_sicof: Optional[Decimal] = None
    page_appropriate_pending: Optional[Decimal] = None
    page_fulfilled: Optional[Decimal] = None
    page_execute_sicof: Optional[Decimal] = None
    page_unfulfilled: Optional[Decimal] = None
    page_value: Optional[Decimal] = None
    page_value_con: Optional[Decimal] = None
    page_total_final_value: Optional[Decimal] = None
    page_total_final_value_con: Optional[Decimal] = None

    class Config:
        from_attributes = True