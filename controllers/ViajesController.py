from typing import Optional
import os
import datetime
from pathlib import Path
import io
import sys
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi import status
from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.AccionesSolicitudAprobacionDTO import AccionSolicitudAprobacion
from dto.ResponseRequest import ResponseRequest
from dto.SolicitudAprobacionHistorialDTO import SolicitudAprobacionHistorialDTOBase
from dto.ViajesDTO import ViajesCalendar, ViajesCreate, TravelLegalizationCreate, TravelLegalizationUpdate, TravelLegalizationResponse
from dto.DocumentosAsociadosDTO import DocumentoAsociadoCreate, DocumentoAsociadoResponse
from services import ViajesService, SolicitudesAprobacionService, SoportesService
from jinja2 import Environment, FileSystemLoader
from entity.travel_requests import TravelRequests
from entity.programs import Programs
from entity.activities import Activities
from entity.rubros import Rubros
from repository.ViajesItinerarioRepository import listar_itinerarios_por_viaje
from html import escape
from services import TravelLegalizationsService
from copy import copy
from types import SimpleNamespace

router = APIRouter(
    prefix='/viajes',
    tags=['Viajes']
)

@router.get("/listados")
def lista_generica(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return ViajesService.lista_generica(db, user_oid)

@router.get("/listados_viajes")
def lista_generica(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return ViajesService.lista_generica_lista_viajes(db)
    
@router.post("", response_model=ResponseRequest)
def crear_viaje(viaje: ViajesCreate, db: DbSession, background_tasks: BackgroundTasks, user_oid: str = Depends(get_current_user_oid)):
    try:

        response_request = ViajesService.crear_viaje(viaje, db, user_oid, background_tasks)
        
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
        # return RolesService.crear_rol(rol, db)
    except HTTPException as e:
        print(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{guid}", response_model=ResponseRequest)
def actualizar_viaje(guid: str, viaje: ViajesCreate, db: DbSession, background_tasks: BackgroundTasks, user_oid: str = Depends(get_current_user_oid)):
    try:

        response_request = ViajesService.actualizar_viaje(guid, viaje, db, user_oid, background_tasks)
        
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
        # return RolesService.crear_rol(rol, db)
    except HTTPException as e:
        print(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("")
def listar_viajes_filtro(
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
    return ViajesService.listar_viajes_por_usuario_sp(db, user_oid, page, filtro, estado, fechaDesde, fechaHasta, programa)
    # return ViajesService.listar_viajes(db, decoded["oid"])


@router.get("/calendario", response_model=list[ViajesCalendar])
def listar_viajes_calendario(
    db: DbSession,
    fechaDesde: datetime.date = Query(...),
    fechaHasta: datetime.date = Query(...),
    user_oid: str = Depends(get_current_user_oid)
) -> list[ViajesCalendar]:
    return ViajesService.listar_viajes_calendario(db, fechaDesde, fechaHasta)


@router.get("/{guid}/detalle", response_model=ViajesCreate)
def obtener_viaje(guid: str, db: DbSession, user_oid: str = Depends(get_current_user_oid)) -> ViajesCreate:
    viaje = ViajesService.obtener_viaje_por_id(guid, db)
    if not viaje:
        raise HTTPException(status_code=404, detail="Viaje no encontrado")
    return viaje

@router.get("/{guid}/validar_acciones_aprobacion")
def validar_acciones_solicitud_aprobacion(guid: str, tipo: str, db: DbSession, user_oid: str = Depends(get_current_user_oid))-> list[SolicitudAprobacionHistorialDTOBase]:
    try:
        viaje = ViajesService.obtener_viaje_por_id(guid, db)
        id_categoria = SolicitudesAprobacionService.obtener_categoria_aprobacion(tipo, db)
        response_request = SolicitudesAprobacionService.validar_habilitar_acciones_solicitud_aprobacion(viaje.id_viaje, id_categoria, user_oid, db, viaje.guid_msft)


        # response_request = ViajesService.crear_viaje(viaje, db, decoded["oid"])
        
        # if response_request.solicitud_exitosa:
        return JSONResponse(
            content=response_request.dict(),
            status_code=status.HTTP_200_OK
        )
        # else:
        #     return JSONResponse(
        #         content=response_request.dict(),
        #         status_code=status.HTTP_200_OK
        #     )
        # return RolesService.crear_rol(rol, db)
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
        viaje = ViajesService.obtener_viaje_por_id(guid, db)
        tipo_solicitud = accion.tipo_solicitud
        id_categoria = SolicitudesAprobacionService.obtener_categoria_aprobacion(tipo_solicitud, db)
        response_request = ViajesService.procesar_accion_solicitud_aprobacion(
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

# def generar_pdf_solicitud(viaje_db: TravelRequests, db: DbSession) -> bytes:
#     # Cargar DLLs de WeasyPrint en Windows si es necesario
#     if os.name == "nt" and hasattr(os, "add_dll_directory"):
#         tesseract_path = r"C:\Program Files\Tesseract-OCR"
#         if os.path.isdir(tesseract_path):
#             try:
#                 os.add_dll_directory(tesseract_path)
#             except Exception as e:
#                 print(f"Error adding DLL directory: {e}")

#     # Configuración para ver los archivos PDF en macOS.
#     if sys.platform == "darwin":
#         import ctypes.util
#         orig_find = ctypes.util.find_library

#         def _custom_find_library(name):
#             res = orig_find(name)
#             if res:
#                 return res
#             search_dirs = ["/opt/homebrew/lib", "/usr/local/lib"]
#             candidates = [name, f"lib{name}" if not name.startswith("lib") else name]
#             suffixes = ["", ".dylib", ".0.dylib", "-0.dylib", ".so"]
#             for d in search_dirs:
#                 for base in candidates:
#                     for suffix in suffixes:
#                         candidate = os.path.join(d, base + suffix)
#                         if os.path.exists(candidate):
#                             return candidate
#             return None

#         ctypes.util.find_library = _custom_find_library

#     from weasyprint import HTML

#     # Cargar nombres/descripciones relacionadas
#     proyecto_name = "N/A"
#     if viaje_db.program_id:
#         program = db.query(Programs).filter(Programs.id == viaje_db.program_id).first()
#         if program:
#             proyecto_name = program.name

#     actividad_name = "N/A"
#     if viaje_db.activity_id:
#         activity = db.query(Activities).filter(Activities.id == viaje_db.activity_id).first()
#         if activity:
#             actividad_name = activity.description

#     rubro_code = viaje_db.short_rubro or "N/A"
#     if (not rubro_code or rubro_code == "N/A") and viaje_db.rubro_id:
#         rubro = db.query(Rubros).filter(Rubros.id == viaje_db.rubro_id).first()
#         if rubro:
#             rubro_code = rubro.rubros

#     solicitante_name = viaje_db.user.full_name if viaje_db.user else "N/A"
#     cargo = viaje_db.user.position if (viaje_db.user and viaje_db.user.position) else ""
#     solicitante_cargo = f"{solicitante_name} - {cargo}" if cargo else solicitante_name

#     # Cargar itinerarios usando el repositorio existente
#     itinerarios_db = listar_itinerarios_por_viaje(viaje_db.travel_request_id, db)
    
#     lugar_ejecucion = viaje_db.location_report or "N/A"
#     if (not lugar_ejecucion or lugar_ejecucion == "N/A") and itinerarios_db:
#         if itinerarios_db[0].destination_municipality:
#             lugar_ejecucion = itinerarios_db[0].destination_municipality.name

#     if viaje_db.is_guest:
#         traveler_name = viaje_db.guest_name
#         traveler_id = viaje_db.guest_document
#         traveler_phone = viaje_db.guest_phone
#         traveler_email = viaje_db.guest_email
#         emergency_name = solicitante_name
#         emergency_phone = viaje_db.user.mobile_phone if viaje_db.user else ""
#         emergency_relation = "Compañero(a) de trabajo"
#     else:
#         traveler_name = solicitante_name
#         traveler_id = viaje_db.user.identification_number if viaje_db.user else ""
#         traveler_phone = viaje_db.user.mobile_phone if viaje_db.user else ""
#         traveler_email = viaje_db.user.email if viaje_db.user else ""
#         emergency_name = ""
#         emergency_phone = ""
#         emergency_relation = ""

#     traveler_id_formatted = ""
#     if traveler_id:
#         try:
#             val = int(str(traveler_id).replace(",", "").replace(".", ""))
#             traveler_id_formatted = f"{val:,}"
#         except:
#             traveler_id_formatted = str(traveler_id)

#     traveler_birth_date = ""
#     if viaje_db.traveler_birth_date:
#         traveler_birth_date = viaje_db.traveler_birth_date.strftime("%m/%d/%Y")

#     fecha_solicitud = ""
#     if viaje_db.created_at:
#         months_es = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
#         dt = viaje_db.created_at
#         fecha_solicitud = f"{dt.day:02d}-{months_es[dt.month - 1]}-{str(dt.year)[-2:]}"

#     itinerario_list = []
#     for it in itinerarios_db:
#         leg_date = ""
#         if it.travel_date:
#             months_es = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
#             leg_date = f"{it.travel_date.day:02d}-{months_es[it.travel_date.month - 1]}-{str(it.travel_date.year)[-2:]}"
        
#         itinerario_list.append({
#             "municipio_origen": it.origin_municipality.name if it.origin_municipality else "",
#             "municipio_destino": it.destination_municipality.name if it.destination_municipality else "",
#             "fecha": leg_date,
#             "hora": it.departure_time or "",
#             "observaciones": it.comments or ""
#         })

#     # Logo local
#     logo_path = Path(__file__).parent.parent.parent / "siva-ii-frontend" / "public" / "images" / "logos" / "logo_patrimonio.png"
#     logo_uri = ""
#     if logo_path.is_file():
#         logo_uri = logo_path.as_uri()

#     template_dir = Path(__file__).parent.parent / "templates"
#     jinja_env = Environment(loader=FileSystemLoader(template_dir))
#     template = jinja_env.get_template("solicitud_viaje.html")

#     html_content = template.render(
#         logo_path=logo_uri,
#         fecha_solicitud=fecha_solicitud,
#         proyecto_name=proyecto_name,
#         actividad_name=actividad_name,
#         rubro_code=rubro_code,
#         solicitante_cargo=solicitante_cargo,
#         lugar_ejecucion=lugar_ejecucion,
#         objetivo=viaje_db.activity_purpose,
#         itinerario=itinerario_list,
#         traveler_name=traveler_name,
#         traveler_id=traveler_id,
#         traveler_id_formatted=traveler_id_formatted,
#         traveler_birth_date=traveler_birth_date,
#         traveler_phone=traveler_phone,
#         traveler_email=traveler_email,
#         emergency_name=emergency_name,
#         emergency_phone=emergency_phone,
#         emergency_relation=emergency_relation
#     )

#     pdf_bytes = HTML(string=html_content).write_pdf()
#     return pdf_bytes

TEMPLATE_DIR = Path(__file__).parent.parent / "templates"
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
WEASYPRINT_WINDOWS_DLL_CANDIDATES = [
    os.getenv("TESSERACT_OCR_PATH")
]
_weasyprint_dll_handles = []
_weasyprint_runtime_initialized = False
url_sistema = os.getenv("url_sistema")
PDF_HEADER_LOGO_URL = f"{url_sistema}/images/logos/logo_patrimonio.png"
pdf_styles_template = env.get_template("pdf_styles.css")
PDF_PAGE_STYLES = pdf_styles_template.render() 
pdf_styles_template = env.get_template("pdf_styles_horizontal.css")
PDF_PAGE_STYLES_HORIZONTAL = pdf_styles_template.render() 



def plantilla_pdf_solicitud_html(viaje, historial_aprobacion_solicitud, end_point: str) -> str:
    template = env.get_template('solicitud_viaje.html')
    return template.render(
        **vars(viaje),
        historialAprobacionSolicitud=historial_aprobacion_solicitud,
        end_point=end_point
    )

def calcular_totales_legalizacion(legalizaciones) -> SimpleNamespace:
    return SimpleNamespace(
        subtotal=sum((legalizacion.subtotal or 0) for legalizacion in legalizaciones),
        iva=sum((legalizacion.iva or 0) for legalizacion in legalizaciones),
        retention=sum((legalizacion.retention or 0) for legalizacion in legalizaciones),
        amount_paid=sum((legalizacion.amount_paid or 0) for legalizacion in legalizaciones),
    )

def plantilla_pdf_legalizacion_html(viaje, historial_aprobacion_solicitud, end_point: str, legalizaciones, documentos_asociados=None) -> str:
    template = env.get_template('legalizacion_viaje.html')
    return template.render(
        **vars(viaje),
        historialAprobacionSolicitud=historial_aprobacion_solicitud,
        end_point=end_point,
        legalizaciones=legalizaciones,
        totales=calcular_totales_legalizacion(legalizaciones),
        documentos_asociados=documentos_asociados
    )

def cargar_clases_weasyprint():
    verificar_entorno_weasyprint()

    try:
        from weasyprint import CSS, HTML
    except OSError as exc:
        detail_msg = (
            "WeasyPrint no pudo cargar las librerias nativas requeridas. "
            "En macOS asegúrese de tener Pango instalado ('brew install pango gdk-pixbuf libffi'). "
            "En Windows configure WEASYPRINT_DLL_DIR apuntando a una carpeta con GTK/Pango."
        )
        raise HTTPException(status_code=500, detail=detail_msg) from exc

    return CSS, HTML


def verificar_entorno_weasyprint() -> None:
    global _weasyprint_runtime_initialized

    if _weasyprint_runtime_initialized:
        return

    if sys.platform == "darwin":
        homebrew_lib_paths = ["/opt/homebrew/lib", "/usr/local/lib"]
        current_dyld = os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "")
        new_paths = [p for p in homebrew_lib_paths if os.path.isdir(p) and p not in current_dyld]
        if new_paths:
            os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = ":".join(new_paths) + (f":{current_dyld}" if current_dyld else "")

    if os.name == "nt" and hasattr(os, "add_dll_directory"):
        seen_paths = set()
        for candidate in WEASYPRINT_WINDOWS_DLL_CANDIDATES:
            if not candidate or not os.path.isdir(candidate):
                continue

            normalized_candidate = os.path.normpath(candidate)
            if normalized_candidate in seen_paths:
                continue

            seen_paths.add(normalized_candidate)
            _weasyprint_dll_handles.append(os.add_dll_directory(normalized_candidate))

    _weasyprint_runtime_initialized = True



def generar_pdf_solicitud(codigo: str, html_out: str) -> bytes:
    return generar_pdf(codigo, html_out)

def generar_pdf_legalizacion(codigo: str, html_out: str) -> bytes:
    CSS, HTML = cargar_clases_weasyprint()
    html_with_pdf_header = (
        '<div class="pdf-page-header-left">'
        f'<img class="pdf-page-header__logo" src="{PDF_HEADER_LOGO_URL}" alt="Logo" />'
        '</div>'
        '<div class="pdf-page-header-right">'
        f'<span class="pdf-page-header__title">FORMATO LEGALIZACIÓN DE ANTICIPO <br>Solicitud Nro: {escape(codigo)}</span>'
        '</div>'
        f'{html_out}'
    )
    css = CSS(string=PDF_PAGE_STYLES_HORIZONTAL)
    return HTML(string=html_with_pdf_header, base_url=str(TEMPLATE_DIR)).write_pdf(
        stylesheets=[css]
    )

def generar_pdf(codigo: str, html_out: str) -> bytes:
    CSS, HTML = cargar_clases_weasyprint()
    html_with_pdf_header = (
        '<div class="pdf-page-header-left">'
        f'<img class="pdf-page-header__logo" src="{PDF_HEADER_LOGO_URL}" alt="Logo" />'
        '</div>'
        '<div class="pdf-page-header-right">'
        f'<span class="pdf-page-header__title">FORMATO SOLICITUD DE TIQUETES PATRIMONIO NATURAL <br>Solicitud Nro: {escape(codigo)}</span>'
        '</div>'
        f'{html_out}'
    )
    css = CSS(string=PDF_PAGE_STYLES)
    return HTML(string=html_with_pdf_header, base_url=str(TEMPLATE_DIR)).write_pdf(
        stylesheets=[css]
    )

def obtener_valor_numerico(valor) -> float:
    return float(valor or 0)

def aplicar_estilo_fila(ws, fila_origen: int, fila_destino: int, columna_inicio: int = 1, columna_fin: int = 12) -> None:
    for col in range(columna_inicio, columna_fin + 1):
        origen = ws.cell(row=fila_origen, column=col)
        destino = ws.cell(row=fila_destino, column=col)
        if origen.has_style:
            destino._style = copy(origen._style)
        if origen.number_format:
            destino.number_format = origen.number_format
        if origen.alignment:
            destino.alignment = copy(origen.alignment)

def agregar_fila_resumen_excel(ws, fila: int, etiqueta: str, valor, fill) -> None:
    ws.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=6)
    ws.cell(row=fila, column=1, value=etiqueta)
    ws.cell(row=fila, column=7, value=valor)
    for columna in range(1, 13):
        ws.cell(row=fila, column=columna).fill = copy(fill)

def generar_excel_facturas_legalizacion(viaje, legalizaciones) -> bytes:
    try:
        from openpyxl import load_workbook
        from openpyxl.styles import PatternFill
    except ImportError as exc:
        raise HTTPException(
            status_code=500,
            detail="La dependencia openpyxl no esta instalada en el backend."
        ) from exc

    plantilla_path = Path(__file__).parent.parent / "static" / "administrativo" / "viajes" / "formato legalizacion.xlsx"
    if not plantilla_path.is_file():
        raise HTTPException(status_code=404, detail="Formato de legalizacion no encontrado")

    wb = load_workbook(plantilla_path)
    ws = wb.active
    fila_encabezado = 6
    fila_inicio = fila_encabezado + 1
    fondo_resumen = PatternFill(fill_type="solid", fgColor="EAF2F8")

    ws["D2"] = viaje.codigo
    ws["D3"] = obtener_valor_numerico(viaje.valor_anticipo) if getattr(viaje, "requiere_anticipo", False) else 0

    for indice, legalizacion in enumerate(legalizaciones):
        fila = fila_inicio + indice
        aplicar_estilo_fila(ws, fila_inicio, fila)

        ws.cell(row=fila, column=1, value=legalizacion.check_date)
        ws.cell(row=fila, column=2, value=legalizacion.check_number)
        ws.cell(row=fila, column=3, value=legalizacion.beneficiary)
        ws.cell(row=fila, column=4, value=legalizacion.nit_beneficiary)
        ws.cell(row=fila, column=5, value=legalizacion.observations_outlay)
        ws.cell(row=fila, column=6, value=legalizacion.regimen_name)
        ws.cell(row=fila, column=7, value=obtener_valor_numerico(legalizacion.subtotal))
        ws.cell(row=fila, column=8, value=obtener_valor_numerico(legalizacion.iva))
        ws.cell(row=fila, column=9, value=obtener_valor_numerico(legalizacion.retention_porcentage))
        ws.cell(row=fila, column=10, value=obtener_valor_numerico(legalizacion.retention))
        ws.cell(row=fila, column=11, value=obtener_valor_numerico(legalizacion.amount_paid))
        ws.cell(row=fila, column=12, value=legalizacion.observations)

    fila_total = fila_inicio + len(legalizaciones)
    aplicar_estilo_fila(ws, fila_inicio, fila_total)
    formula_subtotal = f"=SUM(G{fila_inicio}:G{fila_total - 1})" if legalizaciones else "=0"
    formula_retencion = f"=SUM(J{fila_inicio}:J{fila_total - 1})" if legalizaciones else "=0"
    formula_cancelado = f"=SUM(K{fila_inicio}:K{fila_total - 1})" if legalizaciones else "=0"
    agregar_fila_resumen_excel(ws, fila_total, "TOTAL", formula_subtotal, fondo_resumen)
    ws.cell(row=fila_total, column=10, value=formula_retencion)
    ws.cell(row=fila_total, column=11, value=formula_cancelado)

    filas_resumen = [
        ("TOTAL DINERO CANCELADO", f"=K{fila_total}"),
        ("RETEFUENTE PRACTICADA", f"=J{fila_total}"),
        ("TOTAL GASTO EJECUTADO", None),
        ("TOTAL DINERO CONSIGNADO", None),
        ("PENDIENTE POR REINTEGRAR AL SOLICITANTE", None),
    ]

    for indice, (etiqueta, valor) in enumerate(filas_resumen, start=1):
        fila = fila_total + indice
        aplicar_estilo_fila(ws, fila_inicio, fila)
        if etiqueta == "TOTAL GASTO EJECUTADO":
            valor = f"=G{fila_total + 1}+G{fila_total + 2}"
        elif etiqueta == "TOTAL DINERO CONSIGNADO":
            valor = f"=D3+G{fila_total + 1}"
        elif etiqueta == "PENDIENTE POR REINTEGRAR AL SOLICITANTE":
            valor = f"=IF((G{fila_total + 1}+G{fila_total + 2})>D3,G{fila_total + 1}-G{fila_total + 2}-D3,0)"
        agregar_fila_resumen_excel(ws, fila, etiqueta, valor, fondo_resumen)

    archivo = io.BytesIO()
    wb.save(archivo)
    archivo.seek(0)
    return archivo.getvalue()

@router.get("/{guid}/pdf_solicitud/documento")
def obtener_pdf_solicitud(guid: str, db: DbSession):
    try:
        viaje = ViajesService.obtener_viaje_por_id(guid, db)
        if not viaje:
            raise HTTPException(status_code=404, detail="Viaje no encontrado")
        end_point = f"{os.getenv('url_endpoint')}{os.getenv('endpoint')}"
        id_categoria = SolicitudesAprobacionService.obtener_categoria_aprobacion("SOL_VIA_ANT", db)
        historialAprobacionSolicitud = SolicitudesAprobacionService.obtener_solicitud_aprobacion_por_id_asociado_id_categoria(viaje.id_viaje, id_categoria, db)
        
        html_out = plantilla_pdf_solicitud_html(
            viaje,
            historialAprobacionSolicitud,
            end_point
        )
                
        pdf_bytes = generar_pdf_solicitud(viaje.codigo, html_out)
        
        filename = f"solicitud_{viaje.codigo or viaje.id_viaje}.pdf"
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

@router.post("/{guid}/documento_asociado", response_model=ResponseRequest)
def subir_documento_asociado(
    guid: str,
    documento: DocumentoAsociadoCreate,
    db: DbSession
):
    try:
        viaje_db = db.query(TravelRequests).filter(TravelRequests.guid == guid).first()
        if not viaje_db:
            raise HTTPException(status_code=404, detail="Viaje no encontrado")
            
        nombre_archivo = SoportesService.guardar_documento_viaje(
            codigo_viaje=viaje_db.code,
            base64_data=documento.base64_data,
            db=db,
            travel_request_id=viaje_db.travel_request_id,
            nombre_original=documento.nombre_original,
            document_type_id=documento.document_type_id,
            observaciones=documento.observaciones
        )
        
        return ResponseRequest(
            solicitud_exitosa=True,
            mensaje="Documento guardado exitosamente",
            identity=viaje_db.travel_request_id
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{guid}/documentos_asociados", response_model=list[DocumentoAsociadoResponse])
def listar_documentos_asociados(guid: str, db: DbSession):
    try:
        viaje_db = db.query(TravelRequests).filter(TravelRequests.guid == guid).first()
        if not viaje_db:
            raise HTTPException(status_code=404, detail="Viaje no encontrado")
            
        from repository import SoportesRepository
        registros = SoportesRepository.listar_soportes_por_travel_request_id(viaje_db.travel_request_id, db)
        
        return [
            DocumentoAsociadoResponse(
                id=r.id,
                attachment_name=r.attachment_name,
                document_type_id=r.document_type_id,
                observaciones=r.observations
            ) for r in registros if r.document_type_id in [1, 2]
        ]
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{guid}/archivo/{attachment_id}")
def descargar_archivo_asociado(guid: str, attachment_id: int, db: DbSession):
    from fastapi.responses import FileResponse
    try:
        viaje_db = db.query(TravelRequests).filter(TravelRequests.guid == guid).first()
        if not viaje_db:
            raise HTTPException(status_code=404, detail="Viaje no encontrado")
            
        from entity.attachment_travel_tp import AttachmentTravelTp
        registro = db.query(AttachmentTravelTp).filter(
            AttachmentTravelTp.id == attachment_id,
            AttachmentTravelTp.travel_request_id == viaje_db.travel_request_id
        ).first()
        
        if not registro or not registro.attachment_name:
            raise HTTPException(status_code=404, detail="Archivo no encontrado en BD")
            
        # Intentar con la ruta almacenada o reconstruirla si el entorno cambió
        import os
        from services.SoportesService import SOPORTES_DIR
        
        path_to_use = registro.path_document
        if not path_to_use or not os.path.exists(path_to_use):
            codigo_sanitizado = viaje_db.code
            ruta_esperada = SOPORTES_DIR / codigo_sanitizado / registro.attachment_name
            if os.path.exists(ruta_esperada):
                path_to_use = str(ruta_esperada)
            else:
                raise HTTPException(status_code=404, detail="Archivo no encontrado")
                
        return FileResponse(
            path=path_to_use,
            filename=registro.attachment_name
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/{guid}/pdf_legalizacion/documento")
def obtener_pdf_legalizacion(guid: str, db: DbSession):
    try:
        viaje = ViajesService.obtener_viaje_por_id(guid, db)
        if not viaje:
            raise HTTPException(status_code=404, detail="Viaje no encontrado")
        end_point = f"{os.getenv('url_endpoint')}{os.getenv('endpoint')}"
        id_categoria = SolicitudesAprobacionService.obtener_categoria_aprobacion("SOL_VIA_ANT", db)
        historialAprobacionSolicitud = SolicitudesAprobacionService.obtener_solicitud_aprobacion_por_id_asociado_id_categoria(viaje.id_viaje, id_categoria, db)
        legalizaciones = ViajesService.obtener_legalizaciones_por_viaje(db, viaje.id_viaje)
        
        from repository import SoportesRepository
        registros_soportes = SoportesRepository.listar_soportes_por_travel_request_id(viaje.id_viaje, db)
        documentos_asociados = []
        for r in registros_soportes:
            if r.document_type_id in [1, 2]:
                tipo_archivo = "FACTURA" if r.document_type_id == 1 else ("DOCUMENTO RELACIONADO" if r.document_type_id == 2 else "DESCONOCIDO")
                documentos_asociados.append({
                    "id": r.id,
                    "attachment_name": r.attachment_name,
                    "tipo_archivo": tipo_archivo,
                    "observaciones": r.observations,
                    "url_descarga": f"{end_point}/viajes/{guid}/archivo/{r.id}"
                })

        html_out = plantilla_pdf_legalizacion_html(
            viaje,
            historialAprobacionSolicitud,
            end_point,
            legalizaciones,
            documentos_asociados
        )
                
        pdf_bytes = generar_pdf_legalizacion(viaje.codigo, html_out)
        
        filename = f"legalizacion_{viaje.codigo or viaje.id_viaje}.pdf"
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

@router.get("/{guid}/excel_facturas/documento")
def obtener_excel_facturas_legalizacion(guid: str, db: DbSession):
    try:
        viaje = ViajesService.obtener_viaje_por_id(guid, db)
        if not viaje:
            raise HTTPException(status_code=404, detail="Viaje no encontrado")

        legalizaciones = TravelLegalizationsService.obtener_legalizaciones_por_viaje(db, viaje.id_viaje)
        excel_bytes = generar_excel_facturas_legalizacion(viaje, legalizaciones)
        filename = f"facturas_legalizacion_{viaje.codigo or viaje.id_viaje}.xlsx"

        return StreamingResponse(
            io.BytesIO(excel_bytes),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{guid}/archivo/dos_o_mas_personas")
def descargar_archivo_dos_o_mas_personas(guid: str, db: DbSession):
    from fastapi.responses import FileResponse
    try:
        viaje_db = db.query(TravelRequests).filter(TravelRequests.guid == guid).first()
        if not viaje_db:
            raise HTTPException(status_code=404, detail="Viaje no encontrado")
            
        path_document = SoportesService.obtener_path_document_viaje(viaje_db.travel_request_id, db)
        nombre_archivo = SoportesService.obtener_nombre_archivo_viaje(viaje_db.travel_request_id, db)
        
        if not path_document or not os.path.exists(path_document):
            raise HTTPException(status_code=404, detail="Archivo no encontrado")
            
        return FileResponse(
            path=path_document,
            filename=nombre_archivo,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{guid}/legalizacion", response_model=ResponseRequest)
def guardar_legalizacion(viaje: ViajesCreate, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    try:

        response_request = ViajesService.guardar_legalizacion(viaje, db)
        # response_request = SolicitudesAprobacionService.enviar_solicitud_aprobacion(viaje.id_viaje, 1, decoded["oid"], db)

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

@router.post("/legalizaciones", response_model=ResponseRequest)
@router.post("/legalizaciones/factura", response_model=ResponseRequest, include_in_schema=False)
def crear_factura(
    legalizacion: TravelLegalizationCreate,
    db: DbSession,
    user_oid: str = Depends(get_current_user_oid)
):
    try:
        nuevo = ViajesService.crear_factura(db, legalizacion)
        return ResponseRequest(
            solicitud_exitosa=True,
            mensaje="Factura creada exitosamente",
            identity=nuevo.legalization_id
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear legalización: {str(e)}")

@router.get("/legalizaciones/{travel_request_id}", response_model=list[TravelLegalizationResponse])
def obtener_legalizaciones(
    travel_request_id: int,
    db: DbSession,
    user_oid: str = Depends(get_current_user_oid)
):
    return ViajesService.obtener_legalizaciones_por_viaje(db, travel_request_id)

@router.patch("/legalizaciones/{legalization_id}", response_model=ResponseRequest)
def actualizar_legalizacion(
    legalization_id: int,
    legalizacion: TravelLegalizationUpdate,
    db: DbSession,
    user_oid: str = Depends(get_current_user_oid)
):
    try:
        actualizado = ViajesService.actualizar_legalizacion(db, legalization_id, legalizacion)
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