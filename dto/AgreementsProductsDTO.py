import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class AgreementsProductsBase(BaseModel):
    id: int
    product: str  # objetivo
    code: Optional[str] = None
    quantity: Optional[Decimal] = None
    value: Optional[Decimal] = None
    unit_measure: Optional[str] = None
    shared_ei_one_drive: Optional[str] = None
    observations: Optional[str] = None
    expected_fulfillment_date: Optional[datetime.date] = None
    delivery_date: Optional[datetime.time] = None
    request_date: Optional[datetime.date] = None
    validation_date: Optional[datetime.date] = None
    approval_date: Optional[datetime.date] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    id_agreement: int
    state_id: Optional[int] = None
    id_product: Optional[int] = None  # sin padre es objetivo
    id_duplicate_product: Optional[int] = None
    previous_studies_id: Optional[int] = None
    
    agreement: Optional[str] = None
    product_state: Optional[str] = None
    product_state_color: Optional[str] = None
    previous_study: Optional[str] = None
    
    

    class Config:
        from_attributes = True


class AgreementsProductsCreateBase(BaseModel):
    product: str
    code: Optional[str] = None
    quantity: Optional[Decimal] = None
    value: Optional[Decimal] = None
    unit_measure: Optional[str] = None
    shared_ei_one_drive: Optional[str] = None
    observations: Optional[str] = None
    expected_fulfillment_date: Optional[datetime.date] = None
    delivery_date: Optional[datetime.time] = None
    request_date: Optional[datetime.date] = None
    validation_date: Optional[datetime.date] = None
    approval_date: Optional[datetime.date] = None
    id_agreement: int
    state_id: Optional[int] = None
    id_product: Optional[int] = None
    id_duplicate_product: Optional[int] = None
    previous_studies_id: Optional[int] = None