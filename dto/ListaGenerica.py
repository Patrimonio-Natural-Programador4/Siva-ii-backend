from typing import Optional
from pydantic import BaseModel

class ListaGenerica(BaseModel):
    identity: Optional[int] = None
    valor: Optional[str] = None
    idrelacion: Optional[int] = None
    valorNumerico: Optional[float] = None
    valor_referencia: Optional[str] = None
    valor_referencia2: Optional[str] = None
    valorNumerico2: Optional[float] = None
    aplicaValidacion: Optional[bool] = None
    aplicaSegundaValidacion: Optional[bool] = None
