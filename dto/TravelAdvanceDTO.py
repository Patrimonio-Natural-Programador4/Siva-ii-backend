from typing import Optional
from pydantic import BaseModel  

class TravelAdvanceBase(BaseModel):
    travel_advance_id: Optional[int] = None
    expense_advance_concept_id: Optional[int] = None
    concept: Optional[str] = None
    amount: Optional[float] = None
    observations: Optional[str] = None