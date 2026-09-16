from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional
from datetime import date

class TravelLegalizationCreate(BaseModel):
    travel_request_id: int
    check_date: date
    check_number: Optional[str] = None
    beneficiary: str
    nit_beneficiary: str
    observations_outlay: Optional[str] = None
    regimen_type_id: int
    subtotal: Decimal = Field(..., max_digits=12, decimal_places=2)
    iva: Decimal = Field(..., max_digits=12, decimal_places=2)
    retention_porcentage: Decimal = Field(..., max_digits=5, decimal_places=2)
    retention: Decimal = Field(..., max_digits=12, decimal_places=2)
    amount_paid: Decimal = Field(..., max_digits=12, decimal_places=2)
    observations: Optional[str] = None

class TravelLegalizationUpdate(BaseModel):
    check_date: Optional[date] = None
    check_number: Optional[str] = None
    beneficiary: Optional[str] = None
    nit_beneficiary: Optional[str] = None
    observations_outlay: Optional[str] = None
    regimen_type_id: Optional[int] = None
    subtotal: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    iva: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    retention_porcentage: Optional[Decimal] = Field(None, max_digits=5, decimal_places=2)
    retention: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    amount_paid: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    observations: Optional[str] = None

class TravelLegalizationResponse(TravelLegalizationCreate):
    legalization_id: int
    regimen_name: Optional[str] = None
    created_at: date

    class Config:
        orm_mode = True
