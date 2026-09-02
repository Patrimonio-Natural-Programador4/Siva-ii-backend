from fastapi import APIRouter, Depends, HTTPException, status
from database.database import DbSession
from dto.TravelLegalizationsDto import TravelLegalizationCreate, TravelLegalizationResponse
from services import TravelLegalizationsService
from dependencies.auth_dependency import get_current_user_oid
from dto.ResponseRequest import ResponseRequest

router = APIRouter(
    prefix='/viajes/legalizaciones',
    tags=['Legalizaciones']
)

@router.post("", response_model=ResponseRequest)
def crear_legalizacion(
    legalizacion: TravelLegalizationCreate,
    db: DbSession,
    user_oid: str = Depends(get_current_user_oid)
):
    try:
        nuevo = TravelLegalizationsService.crear_legalizacion(db, legalizacion)
        return ResponseRequest(
            status="SUCCESS",
            message="Legalización creada exitosamente",
            data={"legalization_id": nuevo.legalization_id}
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear legalización: {str(e)}")

@router.get("/{travel_request_id}", response_model=ResponseRequest)
def obtener_legalizacion(
    travel_request_id: int,
    db: DbSession,
    user_oid: str = Depends(get_current_user_oid)
):
    legalizacion = TravelLegalizationsService.obtener_legalizacion_por_viaje(db, travel_request_id)
    if not legalizacion:
        raise HTTPException(status_code=404, detail="Legalización no encontrada para este viaje")
    
    return ResponseRequest(
        status="SUCCESS",
        message="Legalización encontrada",
        data=legalizacion
    )
