from pydantic import BaseModel


class AsignarResponsableAprobacionDTO(BaseModel):
    history_id: int
    user_id: int