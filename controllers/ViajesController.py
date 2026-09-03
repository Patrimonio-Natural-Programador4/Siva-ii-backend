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
from dto.ViajesDTO import ViajesCreate
from services import ViajesService, SolicitudesAprobacionService, SoportesService
from jinja2 import Environment, FileSystemLoader
from entity.travel_requests import TravelRequests
from entity.programs import Programs
from entity.activities import Activities
from entity.rubros import Rubros
from repository.ViajesItinerarioRepository import listar_itinerarios_por_viaje

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

def generar_pdf_solicitud(viaje_db: TravelRequests, db: DbSession) -> bytes:
    # Cargar DLLs de WeasyPrint en Windows si es necesario
    if os.name == "nt" and hasattr(os, "add_dll_directory"):
        tesseract_path = r"C:\Program Files\Tesseract-OCR"
        if os.path.isdir(tesseract_path):
            try:
                os.add_dll_directory(tesseract_path)
            except Exception as e:
                print(f"Error adding DLL directory: {e}")

    # Configuración para ver los archivos PDF en macOS.
    if sys.platform == "darwin":
        import ctypes.util
        orig_find = ctypes.util.find_library

        def _custom_find_library(name):
            res = orig_find(name)
            if res:
                return res
            search_dirs = ["/opt/homebrew/lib", "/usr/local/lib"]
            candidates = [name, f"lib{name}" if not name.startswith("lib") else name]
            suffixes = ["", ".dylib", ".0.dylib", "-0.dylib", ".so"]
            for d in search_dirs:
                for base in candidates:
                    for suffix in suffixes:
                        candidate = os.path.join(d, base + suffix)
                        if os.path.exists(candidate):
                            return candidate
            return None

        ctypes.util.find_library = _custom_find_library

    from weasyprint import HTML

    # Cargar nombres/descripciones relacionadas
    proyecto_name = "N/A"
    if viaje_db.program_id:
        program = db.query(Programs).filter(Programs.id == viaje_db.program_id).first()
        if program:
            proyecto_name = program.name

    actividad_name = "N/A"
    if viaje_db.activity_id:
        activity = db.query(Activities).filter(Activities.id == viaje_db.activity_id).first()
        if activity:
            actividad_name = activity.description

    rubro_code = viaje_db.short_rubro or "N/A"
    if (not rubro_code or rubro_code == "N/A") and viaje_db.rubro_id:
        rubro = db.query(Rubros).filter(Rubros.id == viaje_db.rubro_id).first()
        if rubro:
            rubro_code = rubro.rubros

    solicitante_name = viaje_db.user.full_name if viaje_db.user else "N/A"
    cargo = viaje_db.user.position if (viaje_db.user and viaje_db.user.position) else ""
    solicitante_cargo = f"{solicitante_name} - {cargo}" if cargo else solicitante_name

    # Cargar itinerarios usando el repositorio existente
    itinerarios_db = listar_itinerarios_por_viaje(viaje_db.travel_request_id, db)
    
    lugar_ejecucion = viaje_db.location_report or "N/A"
    if (not lugar_ejecucion or lugar_ejecucion == "N/A") and itinerarios_db:
        if itinerarios_db[0].destination_municipality:
            lugar_ejecucion = itinerarios_db[0].destination_municipality.name

    if viaje_db.is_guest:
        traveler_name = viaje_db.guest_name
        traveler_id = viaje_db.guest_document
        traveler_phone = viaje_db.guest_phone
        traveler_email = viaje_db.guest_email
        emergency_name = solicitante_name
        emergency_phone = viaje_db.user.mobile_phone if viaje_db.user else ""
        emergency_relation = "Compañero(a) de trabajo"
    else:
        traveler_name = solicitante_name
        traveler_id = viaje_db.user.identification_number if viaje_db.user else ""
        traveler_phone = viaje_db.user.mobile_phone if viaje_db.user else ""
        traveler_email = viaje_db.user.email if viaje_db.user else ""
        emergency_name = ""
        emergency_phone = ""
        emergency_relation = ""

    traveler_id_formatted = ""
    if traveler_id:
        try:
            val = int(str(traveler_id).replace(",", "").replace(".", ""))
            traveler_id_formatted = f"{val:,}"
        except:
            traveler_id_formatted = str(traveler_id)

    traveler_birth_date = ""
    if viaje_db.traveler_birth_date:
        traveler_birth_date = viaje_db.traveler_birth_date.strftime("%m/%d/%Y")

    fecha_solicitud = ""
    if viaje_db.created_at:
        months_es = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        dt = viaje_db.created_at
        fecha_solicitud = f"{dt.day:02d}-{months_es[dt.month - 1]}-{str(dt.year)[-2:]}"

    itinerario_list = []
    for it in itinerarios_db:
        leg_date = ""
        if it.travel_date:
            months_es = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
            leg_date = f"{it.travel_date.day:02d}-{months_es[it.travel_date.month - 1]}-{str(it.travel_date.year)[-2:]}"
        
        itinerario_list.append({
            "municipio_origen": it.origin_municipality.name if it.origin_municipality else "",
            "municipio_destino": it.destination_municipality.name if it.destination_municipality else "",
            "fecha": leg_date,
            "hora": it.departure_time or "",
            "observaciones": it.comments or ""
        })

    # Logo local
    logo_path = Path(__file__).parent.parent.parent / "siva-ii-frontend" / "public" / "images" / "logos" / "logo_patrimonio.png"
    logo_uri = ""
    if logo_path.is_file():
        logo_uri = logo_path.as_uri()

    template_dir = Path(__file__).parent.parent / "templates"
    jinja_env = Environment(loader=FileSystemLoader(template_dir))
    template = jinja_env.get_template("solicitud_viaje.html")

    html_content = template.render(
        logo_path=logo_uri,
        fecha_solicitud=fecha_solicitud,
        proyecto_name=proyecto_name,
        actividad_name=actividad_name,
        rubro_code=rubro_code,
        solicitante_cargo=solicitante_cargo,
        lugar_ejecucion=lugar_ejecucion,
        objetivo=viaje_db.activity_purpose,
        itinerario=itinerario_list,
        traveler_name=traveler_name,
        traveler_id=traveler_id,
        traveler_id_formatted=traveler_id_formatted,
        traveler_birth_date=traveler_birth_date,
        traveler_phone=traveler_phone,
        traveler_email=traveler_email,
        emergency_name=emergency_name,
        emergency_phone=emergency_phone,
        emergency_relation=emergency_relation
    )

    pdf_bytes = HTML(string=html_content).write_pdf()
    return pdf_bytes


@router.get("/{guid}/pdf_solicitud/documento")
def obtener_pdf_solicitud(guid: str, db: DbSession):
    try:
        viaje_db = db.query(TravelRequests).filter(TravelRequests.guid == guid).first()
        if not viaje_db:
            raise HTTPException(status_code=404, detail="Viaje no encontrado")
            
        pdf_bytes = generar_pdf_solicitud(viaje_db, db)
        
        filename = f"solicitud_{viaje_db.code or viaje_db.travel_request_id}.pdf"
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

