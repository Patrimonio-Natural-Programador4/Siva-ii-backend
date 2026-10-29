from decimal import Decimal

from pydantic import BaseModel, Field, model_validator


class ProductoDTO(BaseModel):
    modificar: bool = False
    client_id: str | None = Field(default=None, min_length=1, max_length=64)
    id: int | None = Field(default=None, gt=0)
    code: str | None = Field(default=None, max_length=255)
    product: str | None = None
    unit_measure: str | None = None
    quantity: Decimal | None = Field(default=None, ge=0, max_digits=15, decimal_places=2)
    observations: str | None = None

    @model_validator(mode="after")
    def validar_nuevo(self):
        if self.id is None or self.modificar:
            for campo in ("code", "product", "unit_measure"):
                valor = getattr(self, campo)
                if not valor or not valor.strip():
                    raise ValueError(f"El campo {campo} es requerido")
                setattr(self, campo, valor.strip())
            if self.quantity is None:
                raise ValueError("La cantidad es requerida")
        return self


class ActividadDTO(BaseModel):
    modificar: bool = False
    id: int | None = Field(default=None, gt=0)
    code: str | None = Field(default=None, max_length=255)
    product: str | None = None
    productos: list[ProductoDTO] = Field(default_factory=list)

    @model_validator(mode="after")
    def validar_nueva(self):
        if self.id is None or self.modificar:
            if not self.code or not self.code.strip() or not self.product or not self.product.strip():
                raise ValueError("El codigo y el nombre de la actividad son requeridos")
            self.code = self.code.strip()
            self.product = self.product.strip()
        return self


class ObjetivoDTO(BaseModel):
    modificar: bool = False
    id: int | None = Field(default=None, gt=0)
    code: str | None = Field(default=None, max_length=255)
    product: str | None = None
    actividades: list[ActividadDTO] = Field(default_factory=list)

    @model_validator(mode="after")
    def validar_nuevo(self):
        if self.id is None or self.modificar:
            if not self.product or not self.product.strip():
                raise ValueError("El nombre del objetivo es requerido")
            self.product = self.product.strip()
        return self
