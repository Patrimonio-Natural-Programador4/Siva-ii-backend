from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from database.database import DbSession
from dto.TravelLegalizationsDto import TravelLegalizationCreate, TravelLegalizationResponse, TravelLegalizationUpdate
from services import TravelLegalizationsService
from dependencies.auth_dependency import get_current_user_oid
from dto.ResponseRequest import ResponseRequest

router = APIRouter(
    prefix='/viajes/legalizaciones',
    tags=['Legalizaciones']
)

@router.post("", response_model=ResponseRequest)
@router.post("/Legalizacion", response_model=ResponseRequest, include_in_schema=False)
def crear_legalizacion(
    legalizacion: TravelLegalizationCreate,
    db: DbSession,
    user_oid: str = Depends(get_current_user_oid)
):
    try:
        nuevo = TravelLegalizationsService.crear_legalizacion(db, legalizacion)
        return ResponseRequest(
            solicitud_exitosa=True,
            mensaje="Legalización creada exitosamente",
            identity=nuevo.legalization_id
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear legalización: {str(e)}")

@router.get("/{travel_request_id}", response_model=list[TravelLegalizationResponse])
def obtener_legalizaciones(
    travel_request_id: int,
    db: DbSession,
    user_oid: str = Depends(get_current_user_oid)
):
    return TravelLegalizationsService.obtener_legalizaciones_por_viaje(db, travel_request_id)

@router.patch("/{legalization_id}", response_model=ResponseRequest)
def actualizar_legalizacion(
    legalization_id: int,
    legalizacion: TravelLegalizationUpdate,
    db: DbSession,
    user_oid: str = Depends(get_current_user_oid)
):
    try:
        actualizado = TravelLegalizationsService.actualizar_legalizacion(db, legalization_id, legalizacion)
        if not actualizado:
            raise HTTPException(status_code=404, detail="Legalización no encontrada")
        return ResponseRequest(
            solicitud_exitosa=True,
            mensaje="Legalización actualizada exitosamente",
            identity=actualizado.legalization_id
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar legalización: {str(e)}")



