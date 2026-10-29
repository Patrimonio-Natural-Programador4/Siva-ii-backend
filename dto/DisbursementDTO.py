import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class DisbursementBase(BaseModel):
    id: int
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    value: Optional[Decimal] = None
    scheduled_date: Optional[datetime.date] = None
    request_date: Optional[datetime.date] = None
    validation_date: Optional[datetime.date] = None
    approval_date: Optional[datetime.date] = None
    disbursement_date: Optional[datetime.date] = None
    number_disbursement: Optional[int] = None
    documento_soporte: Optional[str] = None
    observations: Optional[str] = None
    state_id: Optional[int] = None
    agreement_id: Optional[int] = None
    previous_studies_id: Optional[int] = None

    class Config:
        from_attributes = True


class DisbursementCreateBase(BaseModel):
    value: Optional[Decimal] = None
    scheduled_date: Optional[datetime.date] = None
    request_date: Optional[datetime.date] = None
    validation_date: Optional[datetime.date] = None
    approval_date: Optional[datetime.date] = None
    disbursement_date: Optional[datetime.date] = None
    number_disbursement: Optional[int] = None
    documento_soporte: Optional[str] = None
    observations: Optional[str] = None
    state_id: Optional[int] = None
    agreement_id: Optional[int] = None
    previous_studies_id: Optional[int] = None