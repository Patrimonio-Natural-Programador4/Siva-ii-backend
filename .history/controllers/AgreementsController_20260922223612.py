# ***************************************
# 1. AgreementsController.py -- 22 Septiembre 2026
# ***************************************

# -----------------------------------------------------------------------------
# BLOQUE 1: Importación de Dependencias, DTOs y Configuración del Router
# -----------------------------------------------------------------------------
# Importa librerías para el manejo de archivos en memoria (io), sistema operativo,
# controladores HTTP de FastAPI, inyección de dependencias de Base de Datos y Autenticación,
# motores de renderizado de plantillas HTML (Jinja2) y conversión a PDF (WeasyPrint).
import io
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.AccionesSolicitudAprobacionDTO import AccionSolicitudAprobacion
from dto.AgreementsDTO import AgreementsCreate, AgreementsFilterDTO
from dto.ResponseRequest import ResponseRequest
from dto.SolicitudAprobacionHistorialDTO import SolicitudAprobacionHistorialDTOBase
from entity.agreements import Agreements
from entity.programs import Programs
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse, StreamingResponse
from jinja2 import Environment, FileSystemLoader
from repository import AgreementItemsRepository, AgreementsRepository
from services import AgreementsService, SolicitudesAprobacionService

# Inicialización del router de FastAPI con el prefijo '/agreements'
router = APIRouter(prefix='/agreements', tags=['Agreements'])


# -----------------------------------------------------------------------------
# BLOQUE 2: Endpoints de Listados y Operaciones CRUD de Convenios
# -----------------------------------------------------------------------------

@router.get('/listados', response_model=ResponseRequest)
def obtener_listados(db: DbSession = Depends()):
    """
    Retorna parametrizaciones, catálogos e información auxiliar 
    necesaria para llenar los desplegables en los formularios de convenios.
    """
    try:
        data = AgreementsService.obtener_listados_parametrizacion(db)
        return ResponseRequest(status=True, message="Listados recuperados exitosamente", data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('', status_code=status.HTTP_201_CREATED)
def crear_convenio(
    convenio: AgreementsCreate,
    background_tasks: BackgroundTasks,
    db: DbSession = Depends(),
    user_oid: str = Depends(get_current_user_oid)
):
    """
    Endpoint para registrar un nuevo convenio. 
    Inyecta el GUID/OID del usuario autenticado e invoca al servicio de creación.
    """
    try:
        nuevo_convenio = AgreementsService.crear_convenio(
            db=db,
            convenio=convenio,
            usuario_guid=user_oid,
            background_tasks=background_tasks
        )
        return ResponseRequest(
            status=True,
            message="Convenio creado correctamente",
            data={"guid": nuevo_convenio.guid, "codigo_siva": nuevo_convenio.codigo_siva}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/{guid}')
def actualizar_convenio(
    guid: str,
    convenio: AgreementsCreate,
    db: DbSession = Depends(),
    user_oid: str = Depends(get_current_user_oid)
):
    """
    Endpoint para modificar la información de un convenio existente mediante su GUID.
    """
    try:
        convenio_actualizado = AgreementsService.actualizar_convenio(
            db=db,
            convenio_guid=guid,
            convenio=convenio,
            usuario_guid=user_oid
        )
        return ResponseRequest(status=True, message="Convenio actualizado correctamente", data={"guid": convenio_actualizado.guid})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('')
def listar_convenios(
    filtro: Optional[str] = Query(None),
    p_page: int = Query(1, ge=1),
    p_page_size: int = Query(25, ge=1),
    db: DbSession = Depends()
):
    """
    Endpoint de consulta paginada de convenios. Executa el procedimiento almacenado
    a través del repositorio 'AgreementsRepository'.
    """
    try:
        resultado = AgreementsRepository.listar_convenios_sp(
            db=db,
            p_search=filtro,
            p_page=p_page,
            p_page_size=p_page_size
        )
        return ResponseRequest(status=True, message="Convenios consultados", data=resultado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/{guid}/detalle')
def obtener_detalle_convenio(guid: str, db: DbSession = Depends()):
    """
    Recupera la información completa y detallada de un convenio específico.
    """
    try:
        convenio_detalle = AgreementsService.obtener_convenio_por_id(db, guid)
        return ResponseRequest(status=True, message="Detalle de convenio obtenido", data=convenio_detalle)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# -----------------------------------------------------------------------------
# BLOQUE 3: Integración con el Motor de Flujos de Aprobación
# -----------------------------------------------------------------------------

@router.get('/{guid}/validar_acciones_aprobacion')
def validar_acciones_aprobacion(
    guid: str,
    db: DbSession = Depends(),
    user_oid: str = Depends(get_current_user_oid)
):
    """
    Valida y consulta qué acciones de aprobación (Aprobar, Rechazar, Devolver) 
    tiene habilitadas el usuario actual sobre el convenio especificado.
    """
    try:
        convenio = db.query(Agreements).filter(Agreements.guid == guid).first()
        if not convenio or not convenio.approval_request_id:
            return ResponseRequest(status=False, message="El convenio no posee un flujo de aprobación activo", data={})

        # Consulta al servicio unificado de aprobaciones
        acciones = SolicitudesAprobacionService.validar_habilitar_acciones_solicitud_aprobacion(
            db=db,
            solicitud_id=convenio.approval_request_id,
            usuario_oid=user_oid
        )
        return ResponseRequest(status=True, message="Acciones de aprobación consultadas", data=acciones)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/{guid}/accion_solicitud_aprobacion')
def ejecutar_accion_aprobacion(
    guid: str,
    accion_dto: AccionSolicitudAprobacion,
    db: DbSession = Depends(),
    user_oid: str = Depends(get_current_user_oid)
):
    """
    Procesa la decisión tomada por un aprobador/supervisor (ej. Aprobado o Rechazado)
    y actualiza el estado general del convenio en consecuencia.
    """
    try:
        convenio = db.query(Agreements).filter(Agreements.guid == guid).first()
        if not convenio or not convenio.approval_request_id:
            raise HTTPException(status_code=400, detail="El convenio no tiene una solicitud de aprobación vinculada")

        # Procesa la acción en el motor de aprobaciones
        resultado = SolicitudesAprobacionService.procesar_accion_solicitud_aprobacion(
            db=db,
            solicitud_id=convenio.approval_request_id,
            accion_dto=accion_dto,
            usuario_oid=user_oid
        )

        return ResponseRequest(status=True, message="Acción de aprobación procesada exitosamente", data=resultado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------------------------------------------
# BLOQUE 4: Generación y Descarga de Documento PDF (WeasyPrint / Jinja2)
# -----------------------------------------------------------------------------

@router.get('/{guid}/pdf_solicitud/documento')
def generar_pdf_convenio(guid: str, db: DbSession = Depends()):
    """
    Compila dinámicamente una plantilla HTML con Jinja2 cargando la información 
    del convenio e ítems, y la convierte en un documento PDF imprimible en streaming mediante WeasyPrint.
    """
    try:
        # Importación diferida de WeasyPrint para optimizar el arranque del servidor
        from weasyprint import HTML

        # 1. Obtención de datos del convenio, programa e ítems asociados
        convenio = db.query(Agreements).filter(Agreements.guid == guid).first()
        if not convenio:
            raise HTTPException(status_code=404, detail="Convenio no encontrado")

        programa = db.query(Programs).filter(Programs.id == convenio.program_id).first()
        items = AgreementItemsRepository.obtener_items_por_convenio_id(db, convenio.id)

        # 2. Configuración del entorno de plantillas Jinja2
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("solicitud_convenio.html")

        # 3. Renderizado de la plantilla HTML con las variables del convenio
        html_rendered = template.render(
            codigo_siva=convenio.codigo_siva,
            nombre_convenio=convenio.nombre_convenio,
            objeto_acuerdo=convenio.objeto_acuerdo,
            programa_nombre=programa.nombre if programa else "N/A",
            fecha_generacion=datetime.now().strftime("%d/%m/%Y"),
            items=items
        )

        # 4. Conversión de HTML a binario PDF mediante WeasyPrint
        pdf_bytes = HTML(string=html_rendered).write_pdf()

        # 5. Envío del archivo como flujo StreamingResponse para visualización/descarga
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f"inline; filename=Solicitud_{convenio.codigo_siva}.pdf"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar el PDF: {str(e)}")