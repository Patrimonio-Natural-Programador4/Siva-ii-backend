from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID


class ContractsBase(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    description: Optional[str] = None
    year: Optional[int] = None
    start_contract_date: Optional[date] = None
    end_contract_date: Optional[date] = None
    subscription_date: Optional[date] = None
    policy_date: Optional[date] = None
    final_date: Optional[date] = None
    early_settlement_date: Optional[date] = None
    identification_type: Optional[str] = None
    identification_number: Optional[str] = None
    bank_code: Optional[str] = None
    bank_account: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    mobile_phone: Optional[str] = None
    programa: Optional[str] = None
    program_id: Optional[int] = None
    contract_type: Optional[str] = None
    contract_type_id: Optional[int] = None
    pillar: Optional[str] = None
    pillar_id: Optional[int] = None
    expense_category: Optional[str] = None
    expense_category_id: Optional[int] = None
    purchase_type: Optional[str] = None
    purchase_type_id: Optional[int] = None
    contract_id: Optional[int] = None
    terms_reference_id: Optional[int] = None
    is_currency_usd: Optional[bool] = None
    policy_approval: Optional[bool] = None
    observations: Optional[str] = None
    causes_early_termination: Optional[str] = None
    sharepoint_code_new: Optional[str] = None
    functions_and_activities: Optional[str] = None
    dibursement: Optional[str] = None
    monthly_time: Optional[float] = None
    final_duration: Optional[float] = None
    value: Optional[float] = None
    initial_value: Optional[float] = None
    final_value: Optional[float] = None
    total_adition: Optional[float] = None
    released_resource: Optional[float] = None
    last_dibursement: Optional[int] = None
    dibursement_value: Optional[float] = None
    total_value: Optional[float] = None
    accumulated_value: Optional[float] = None
    remaining_value: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True




class ContractsCreate(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None
    year: Optional[int] = None
    start_contract_date: Optional[date] = None
    end_contract_date: Optional[date] = None
    subscription_date: Optional[date] = None
    policy_date: Optional[date] = None
    final_date: Optional[date] = None
    identification_type: Optional[str] = None
    identification_number: Optional[str] = None
    bank_code: Optional[str] = None
    bank_account: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    mobile_phone: Optional[str] = None
    program_id: Optional[int] = None
    contract_type_id: Optional[int] = None
    pillar_id: Optional[int] = None
    expense_category_id: Optional[int] = None
    purchase_type_id: Optional[int] = None
    contract_id: Optional[int] = None
    terms_reference_id: Optional[int] = None
    is_currency_usd: Optional[bool] = False
    policy_approval: Optional[bool] = False
    observations: Optional[str] = None
    functions_and_activities: Optional[str] = None
    dibursement: Optional[str] = None
    value: Optional[float] = None
    initial_value: Optional[float] = None

    class Config:
        from_attributes = True


   


class ContractListSP(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    description: Optional[str] = None
    line_paa: Optional[int] = None
    line_pad: Optional[int] = None
    year: Optional[int] = None
    start_contract_date: Optional[date] = None
    end_contract_date: Optional[date] = None
    bank_code: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    mobile_phone: Optional[str] = None
    program_name: Optional[str] = None
    is_currency_usd: Optional[bool] = None
    contract_type_name: Optional[str] = None
    pillar_name: Optional[str] = None
    expense_category_name: Optional[str] = None
    purchase_type_name: Optional[str] = None
    observations: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    policy_approval: Optional[bool] = None
    policy_date: Optional[date] = None
    final_date: Optional[date] = None
    early_settlement_date: Optional[date] = None
    causes_early_termination: Optional[str] = None
    released_resource: Optional[float] = None
    value: Optional[float] = None
    total_adition: Optional[float] = None
    last_dibursement: Optional[int] = None
    dibursement_value: Optional[float] = None
    accumulated_value: Optional[float] = None
    settle_value: Optional[float] = None
    remaining_value: Optional[float] = None
    total_restante: Optional[float] = None
    can_delete: Optional[bool] = None
    grand_released_resource: Optional[float] = None
    grand_value: Optional[float] = None
    grand_total_adition: Optional[float] = None
    grand_dibursement_value: Optional[float] = None
    grand_accumulated_value: Optional[float] = None
    grand_settle_value: Optional[float] = None
    grand_remaining_value: Optional[float] = None
    grand_total_restante: Optional[float] = None
    total_records: Optional[int] = None
    page_released_resource: Optional[float] = None
    page_value: Optional[float] = None
    page_total_adition: Optional[float] = None
    page_dibursement_value: Optional[float] = None
    page_accumulated_value: Optional[float] = None
    page_settle_value: Optional[float] = None
    page_remaining_value: Optional[float] = None
    page_total_restante: Optional[float] = None

    class Config:
        from_attributes = True
        
        
        
