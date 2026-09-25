from typing import Optional
import os
import datetime
from pathlib import Path
import io

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi import status

# Inyección de Base de Datos y Autenticación de tu entorno
from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid

# DTOs
from dto.ResponseRequest import ResponseRequest
from dto.AccionesSolicitudAprobacionDTO import AccionSolicitudAprobacion
from dto.SolicitudAprobacionHistorialDTO import SolicitudAprobacionHistorialDTOBase
from dto.AgreementsDTO import AgreementsCreate

# Servicios
from services import AgreementsService, SolicitudesAprobacionService

# Entidades ORM para el reporte PDF
from entity.agreements import Agreements
from entity.programs import Programs
from repository.AgreementItemsRepository import listar_por_convenio

from jinja2 import Environment, FileSystemLoader

router = APIRouter(
    prefix='/agreements',
    tags=['Agreements']
)


@router.get("/listados")
def lista_generica(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return AgreementsService.lista_generica(db, user_oid)


@router.post("", response_model=ResponseRequest)
def crear_convenio(
    convenio: AgreementsCreate, 
    db: DbSession, 
    background_tasks: BackgroundTasks, 
    user_oid: str = Depends(get_current_user_oid)
):
    try:
        response_request = AgreementsService.crear_convenio(convenio, db, user_oid, background_tasks)
        
        if response_request.solicitud_exitosa:
            return JSONResponse(
                content=response_request.dict(),
                status_code=status.HTTP_201_CREATED
            )
        else:
            return JSONResponse(
                content=response_request.dict(),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    except HTTPException as e:
        print(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{guid}", response_model=ResponseRequest)
def actualizar_convenio(
    guid: str, 
    convenio: AgreementsCreate, 
    db: DbSession, 
    background_tasks: BackgroundTasks, 
    user_oid: str = Depends(get_current_user_oid)
):
    try:
        response_request = AgreementsService.actualizar_convenio(guid, convenio, db, user_oid, background_tasks)
        
        if response_request.solicitud_exitosa:
            return JSONResponse(
                content=response_request.dict(),
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content=response_request.dict(),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    except HTTPException as e:
        print(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("")
def listar_convenios_filtro(
    db: DbSession,
    page: int = Query(...),
    filtro: str = Query(...),
    estado: list[int] = Query(...),
    fechaDesde: Optional[str] = Query(None),
    fechaHasta: Optional[str] = Query(None),
    programa: Optional[int] = Query(None),
    user_oid: str = Depends(get_current_user_oid)
):
    if fechaDesde == "null":
        fechaDesde = None

    if fechaHasta == "null":
        fechaHasta = None

    return AgreementsService.listar_convenios_por_usuario_sp(
        db, user_oid, page, filtro, estado, fechaDesde, fechaHasta, programa
    )


@router.get("/{guid}/detalle", response_model=AgreementsCreate)
def obtener_convenio(guid: str, db: DbSession, user_oid: str = Depends(get_current_user_oid)) -> AgreementsCreate:
    convenio = AgreementsService.obtener_convenio_por_id(guid, db)
    if not convenio:
        raise HTTPException(status_code=404, detail="Convenio no encontrado")
    return convenio


@router.get("/{guid}/validar_acciones_aprobacion")
def validar_acciones_solicitud_aprobacion(
    guid: str, 
    tipo: str, 
    db: DbSession, 
    user_oid: str = Depends(get_current_user_oid)
) -> list[SolicitudAprobacionHistorialDTOBase]:
    try:
        convenio = AgreementsService.obtener_convenio_por_id(guid, db)
        id_categoria = SolicitudesAprobacionService.obtener_categoria_aprobacion(tipo, db)
        response_request = SolicitudesAprobacionService.validar_habilitar_acciones_solicitud_aprobacion(
            convenio.id_convenio, id_categoria, user_oid, db, convenio.guid_msft
        )

        return JSONResponse(
            content=response_request.dict(),
            status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        print(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{guid}/accion_solicitud_aprobacion", response_model=ResponseRequest)
def accion_solicitud_aprobacion(
    guid: str,
    accion: AccionSolicitudAprobacion,
    db: DbSession,
    background_tasks: BackgroundTasks,
    user_oid: str = Depends(get_current_user_oid)
):
    try:
        convenio = AgreementsService.obtener_convenio_por_id(guid, db)
        tipo_solicitud = accion.tipo_solicitud
        id_categoria = SolicitudesAprobacionService.obtener_categoria_aprobacion(tipo_solicitud, db)
        response_request = AgreementsService.procesar_accion_solicitud_aprobacion(
            accion, user_oid, id_categoria, db, background_tasks
        )
        return JSONResponse(
            content=response_request.dict(),
            status_code=status.HTTP_200_OK if response_request.solicitud_exitosa else status.HTTP_400_BAD_REQUEST
        )
    except HTTPException as e:
        print(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def generar_pdf_convenio(convenio_db: Agreements, db: DbSession) -> bytes:
    # Cargar DLLs de WeasyPrint en Windows si aplica
    if os.name == "nt" and hasattr(os, "add_dll_directory"):
        tesseract_path = r"C:\Program Files\Tesseract-OCR"
        if os.path.isdir(tesseract_path):
            try:
                os.add_dll_directory(tesseract_path)
            except Exception as e:
                print(f"Error adding DLL directory: {e}")

    from weasyprint import HTML

    proyecto_name = "N/A"
    if convenio_db.program_id:
        program = db.query(Programs).filter(Programs.id == convenio_db.program_id).first()
        if program:
            proyecto_name = program.name

    solicitante_name = convenio_db.created_by_user.full_name if convenio_db.created_by_user else "N/A"

    # Cargar ítems asociados al convenio
    items_db = listar_por_convenio(convenio_db.agreement_id, db)
    items_list = []
    for item in items_db:
        items_list.append({
            "descripcion": item.description,
            "monto": item.amount
        })

    fecha_creacion = ""
    if convenio_db.created_at:
        months_es = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        dt = convenio_db.created_at
        fecha_creacion = f"{dt.day:02d}-{months_es[dt.month - 1]}-{str(dt.year)[-2:]}"

    # Cargar logo de la organización
    logo_path = Path(__file__).parent.parent.parent / "siva-ii-frontend" / "public" / "images" / "logos" / "logo_patrimonio.png"
    logo_uri = logo_path.as_uri() if logo_path.is_file() else ""

    template_dir = Path(__file__).parent.parent / "templates"
    jinja_env = Environment(loader=FileSystemLoader(template_dir))
    template = jinja_env.get_template("solicitud_convenio.html")

    html_content = template.render(
        logo_path=logo_uri,
        codigo=convenio_db.code,
        titulo=convenio_db.title,
        descripcion=convenio_db.description,
        fecha_creacion=fecha_creacion,
        fecha_inicio=convenio_db.start_date.strftime("%Y-%m-%d") if convenio_db.start_date else "",
        fecha_fin=convenio_db.end_date.strftime("%Y-%m-%d") if convenio_db.end_date else "",
        proyecto_name=proyecto_name,
        solicitante_name=solicitante_name,
        items=items_list
    )

    pdf_bytes = HTML(string=html_content).write_pdf()
    return pdf_bytes


@router.get("/{guid}/pdf_solicitud/documento")
def obtener_pdf_convenio(guid: str, db: DbSession):
    try:
        convenio_db = db.query(Agreements).filter(Agreements.guid == guid).first()
        if not convenio_db:
            raise HTTPException(status_code=404, detail="Convenio no encontrado")
            
        pdf_bytes = generar_pdf_convenio(convenio_db, db)
        
        filename = f"convenio_{convenio_db.code or convenio_db.agreement_id}.pdf"
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f"inline; filename={filename}"}
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))