from dto.SolicitudAprobacionHistorialDTO import SolicitudAprobacionHistorialDTOBase
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status, Request
from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from services import SolicitudesAprobacionService

router = APIRouter(
    prefix='/solicitudes-aprobacion',
    tags=['SolicitudesAprobacion']
)


@router.get("/historial_aprobacion")
def historial_aprobacion(
    db: DbSession,
    guid: str = Query(...),
    tipo_solicitud: str = Query(...),
    user_oid: str = Depends(get_current_user_oid)
) -> list[SolicitudAprobacionHistorialDTOBase]:
    id_categoria = SolicitudesAprobacionService.obtener_categoria_aprobacion(tipo_solicitud, db)
    return SolicitudesAprobacionService.obtener_solicitud_aprobacion_por_id_asociado_id_categoria(guid, id_categoria, db)