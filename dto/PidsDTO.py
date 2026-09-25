from typing import Optional
from pydantic import BaseModel, Field


class PidsBase(BaseModel):
    id:         Optional[int] = None
    pad_id:     Optional[int] = None
    name:       Optional[str] = None
    description:Optional[str] = None
    color:      Optional[str] = None
  
    pad:      Optional[str] = None
    eur_usd_rate: Optional[float] = None
    usd_cop_rate: Optional[float] = None
    eur_cop_rate: Optional[float] = None
    sicof_code:   Optional[str] = None
    
    class Config:
        from_attributes = True

# DTO listar docs
class PidsListDTO(BaseModel):
    id:            int
    name:          str
    description:   str
    color:         str
    eur_usd_rate:  float
    usd_cop_rate:  float
    eur_cop_rate:  float
    sicof_code:    float
    pad_id:        str
    
    class Config:
        from_attributes = True
