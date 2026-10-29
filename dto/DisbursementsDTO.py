from datetime import date
from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator, model_validator


class DesembolsoDTO(BaseModel):
    id: int | None = Field(default=None, gt=0)
    number_disbursement: int | None = Field(default=None, ge=1, le=2147483647)
    scheduled_date: Optional[date] | None = None
    value: Decimal | None = Field(default=None, ge=0, max_digits=15, decimal_places=2)
    state_id: int | None = Field(default=1, gt=0)
    request_date: date | None = None
    validation_date: date | None = None
    approval_date: date | None = None
    disbursement_date: date | None = None
    documento_soporte: str | None = None
    observations: str | None = None
    product_keys: list[str] = Field(default_factory=list)

    @field_validator("request_date", "validation_date", "approval_date", "disbursement_date", mode="before")
    @classmethod
    def fecha_opcional(cls, valor):
        return None if valor == "" else valor

    @model_validator(mode="after")
    def validar_nuevo(self):
        if self.id is None:
            if self.number_disbursement is None or self.value is None:
                raise ValueError("El numero y el valor son requeridos")
        if self.id is None or "product_keys" in self.model_fields_set:
            if not self.product_keys:
                raise ValueError("Debe seleccionar al menos un producto")
        if len(set(self.product_keys)) != len(self.product_keys):
            raise ValueError("No se puede repetir un producto en el desembolso")
        return self
