#CONTROLADOR ESTUDIOS PREVIOS CON NOTIFICAIONES
import io
import os
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi import status
from jinja2 import Environment, FileSystemLoader
from dto.ResponseRequest import ResponseRequest
from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid

from dto.AccionesSolicitudAprobacionDTO import AccionSolicitudAprobacion
from entity.implementers import Implementers
from entity.persons import Persons
from entity.previous_studies_states import PreviousStudiesStates
from services import PreviousStudiesService, SolicitudesAprobacionService
from repository import PreviousStudiesRepository
from dto.PreviousStudiesDTO import PreviousStudiesCreate
from services import PreviousStudiesService
from entity.previous_studies import PreviousStudies as PreviousStudiesEntity
from entity.programs import Programs

CATEGORIA_APROBACION = "APP_EP"

router = APIRouter(
    prefix='/estudios-previos',
    tags=['EstudiosPrevios']
)


@router.get('')
def listar(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return PreviousStudiesService.listar(db)


@router.get("/filtro")
def listar_previous_studies_filtro(
    db: DbSession,
    user_oid: str = Depends(get_current_user_oid),
    page: int = Query(...),
    estado: list[int] = Query([-1]),
    programa: Optional[int] = Query(-1),
    filtro: str = Query(""),
):
    try:
        return PreviousStudiesService.listar_previous_studies_por_usuario_sp(
            db, user_oid, page, estado, filtro, programa
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get('/{id}')
def obtener_estudio_por_id(id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    estudio = PreviousStudiesService.obtener_est_previo_por_id(id, db)
    if not estudio:
        raise HTTPException(status_code=404, detail='Estudio previo no encontrado')
    return estudio

@router.post('', response_model=ResponseRequest)
def crear_estudio(payload: PreviousStudiesCreate, db: DbSession,background_tasks: BackgroundTasks, user_oid: str = Depends(get_current_user_oid)):
    try:
        response_request = PreviousStudiesService.crearEstudioPrevio(payload, db, user_oid, background_tasks)

        if response_request.solicitud_exitosa:
            return JSONResponse(
                content=response_request.model_dump(),
                status_code=status.HTTP_201_CREATED
            )
        else:
            return JSONResponse(
                content=response_request.model_dump(),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    except HTTPException as e:
        print(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))  
    
@router.get('/{guid}/detalle')
def obtener_por_guid(guid: str, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    estudio = PreviousStudiesService.obtener_por_guid(guid, db)
    if not estudio:
        raise HTTPException(status_code=404, detail='Estudio previo no encontrado')
    print('ESTUDIOOO', estudio)
    return estudio


@router.get('/{guid}/validar_acciones_aprobacion')
def validar_acciones_solicitud_aprobacion(guid: str, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    try:
        estudio = PreviousStudiesService.obtener_por_guid(guid, db)
        if not estudio:
            raise HTTPException(status_code=404, detail='Estudio previo no encontrado')
        id_categoria = SolicitudesAprobacionService.obtener_categoria_aprobacion(CATEGORIA_APROBACION, db)
        respuesta = SolicitudesAprobacionService.validar_habilitar_acciones_solicitud_aprobacion(
            estudio.id, id_categoria, user_oid, db
        )
        return JSONResponse(content=respuesta.model_dump(), status_code=status.HTTP_200_OK)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/{guid}/accion_solicitud_aprobacion', response_model=ResponseRequest)
def accion_solicitud_aprobacion(
    guid: str,
    accion: AccionSolicitudAprobacion,
    db: DbSession,
    background_tasks: BackgroundTasks,
    user_oid: str = Depends(get_current_user_oid),
):
    try:
        estudio_db = PreviousStudiesRepository.obtener_por_guid(guid, db)
        if not estudio_db:
            raise HTTPException(status_code=404, detail='Estudio previo no encontrado')

        if accion.estudio_previo is None:
            accion.estudio_previo = PreviousStudiesCreate()

        accion.estudio_previo.id = estudio_db.id
        accion.estudio_previo.guid = estudio_db.guid
        accion.id_solicitud_aprobacion = estudio_db.approval_request_id

        id_categoria = SolicitudesAprobacionService.obtener_categoria_aprobacion(CATEGORIA_APROBACION, db)
        respuesta = PreviousStudiesService.procesar_accion_solicitud_aprobacion(
            accion, user_oid, id_categoria, db, background_tasks
        )
        return JSONResponse(
            content=respuesta.model_dump(),
            status_code=status.HTTP_200_OK if respuesta.solicitud_exitosa else status.HTTP_400_BAD_REQUEST,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.put('/{guid}', response_model=ResponseRequest)
def actualizar_estudio(guid: str, payload: PreviousStudiesCreate, db: DbSession,background_tasks: BackgroundTasks, user_oid: str = Depends(get_current_user_oid)):
    try:
        estudio_db = PreviousStudiesRepository.obtener_por_guid(guid, db)
        if not estudio_db:
            raise HTTPException(status_code=404, detail='Estudio previo no encontrado')
        response_request = PreviousStudiesService.actualizar(estudio_db.id, payload, db, user_oid, background_tasks)
        return JSONResponse(
            content=response_request.model_dump(),
            status_code=status.HTTP_200_OK if response_request.solicitud_exitosa else status.HTTP_400_BAD_REQUEST
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
def generar_pdf_solicitud_EP(estudio_db: PreviousStudiesEntity, db: DbSession) -> bytes:
    # Cargar DLLs de WeasyPrint en Windows si es necesario
    if os.name == "nt" and hasattr(os, "add_dll_directory"):
        tesseract_path = r"C:\Program Files\Tesseract-OCR"
        if os.path.isdir(tesseract_path):
            try:
                os.add_dll_directory(tesseract_path)
            except Exception as e:
                print(f"Error adding DLL directory: {e}")

    from weasyprint import HTML

    # Cargar nombres/descripciones relacionadas
    
           
    precedents = estudio_db.precedents if estudio_db.precedents else ""
    justification = estudio_db.justification if estudio_db.justification else ""
    scope = estudio_db.scope if estudio_db.scope else ""
    overall_objective = estudio_db.scope if estudio_db.scope else ""
    term = estudio_db.term if estudio_db.term else ""
    obligations = estudio_db.obligations if estudio_db.obligations else ""
    supervisor = estudio_db.supervisor if estudio_db.supervisor else ""
    estimated_term= estudio_db.estimated_term if estudio_db.estimated_term else ""
      
    
     # CAPACITY ASSESMENTS
    capacity_name = "N/A"
    if estudio_db.program_id:
        program = db.query(Programs).filter(Programs.id == estudio_db.program_id).first()
        if program:
            capacity_name = program.name 
            
    #IMPLEMENTER
    implementer_name = "N/A"
    if estudio_db.implementer_id:
        implementer = db.query(Implementers).filter(Implementers.id == estudio_db.implementer_id).first()
        if implementer:
            implementer_name = implementer.acronym       
    

# RESPONSABLE
    
    leader_name = "N/A"
    if estudio_db.persons_id:
        person = db.query(Persons).filter(Persons.id == estudio_db.persons_id).first()
        if person:
            fullname= "{fname}  {lname} {olname}".format(fname = person.first_name, lname =person.last_name, olname =person.other_last_name)
            leader_name = fullname

    
    # PROGRAMA
    programa_name = "N/A"
    if estudio_db.program_id:
        program = db.query(Programs).filter(Programs.id == estudio_db.program_id).first()
        if program:
            programa_name = program.name

    #ESTADO EVALUACION DE CAPACIDAD
        previous_studies_state_name = "N/A"
        if estudio_db.previous_studies_states_id:
            estado_estudio = db.query(PreviousStudiesStates).filter(PreviousStudiesStates.id == estudio_db.previous_studies_states_id).first()
            if estado_estudio:
                previous_studies_state_name = estado_estudio.state

   # VALOS
    total_value = f"{estudio_db.total_value:,.0f}" if estudio_db.total_value else "0"
    contributions_fpn = f"{estudio_db.contributions_fpn:,.0f}" if estudio_db.contributions_fpn else "0"
    contributions_ei = f"{estudio_db.contributions_ei:,.0f}" if estudio_db.contributions_ei else "0"
    total_value_executes_fpn = f"{estudio_db.total_value_executes_fpn:,.0f}" if estudio_db.total_value_executes_fpn else "0"
    total_value_executes_ei = f"{estudio_db.total_value_executes_ei:,.0f}" if estudio_db.total_value_executes_ei else "0"
        
    
    # Logo local
    logo_path = Path(__file__).parent.parent.parent / "siva-ii-frontend" / "public" / "images" / "logos" / "logo_patrimonio.png"
    logo_uri = ""
    if logo_path.is_file():
        logo_uri = logo_path.as_uri()

    template_dir = Path(__file__).parent.parent / "templates"
    jinja_env = Environment(loader=FileSystemLoader(template_dir))
    template = jinja_env.get_template("estudios_previos.html")

    html_content = template.render(
        logo_path=logo_uri,
        precedents=precedents,
        justification=justification,
        scope=scope,
        overall_objective=overall_objective,
        term=term,
        obligations=obligations,
        supervisor=supervisor,
        estimated_term=estimated_term,
        previous_studies_state_name=previous_studies_state_name,
        total_value=total_value,
        contributions_fpn = contributions_fpn,
        contributions_ei=contributions_ei,
        total_value_executes_fpn = total_value_executes_fpn,
        total_value_executes_ei =total_value_executes_ei,
        programa=programa_name,
        implementer=implementer_name,
        leader_name=leader_name,
        capacity_name= capacity_name,
        
        
    )

    pdf_bytes = HTML(string=html_content).write_pdf()
    return pdf_bytes


@router.get("/{guid}/pdf_solicitud/documento")
def obtener_pdf_solicitud_EP(guid: str, db: DbSession):
    try:
        estudio_db = db.query(PreviousStudiesEntity).filter(PreviousStudiesEntity.guid == guid).first()
        if not estudio_db:
            raise HTTPException(status_code=404, detail="Estudio no encontrado")
            
        pdf_bytes = generar_pdf_solicitud_EP(estudio_db, db)
        
        filename = f"solicitud_{estudio_db.app_request or estudio_db.PreviousStudiesEntity}.pdf"
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