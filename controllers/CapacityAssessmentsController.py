import io
import os
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException,Query
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi import status
from typing import Optional

from jinja2 import Environment, FileSystemLoader

from database.database import DbSession
from dependencies.auth_dependency import get_current_user_oid
from dto.CapacityAssessmentsDTO import CapacityAssessmentsBase,CapacityAssessmentsCreate
from dto.ResponseRequest import ResponseRequest
from entity.implementers import Implementers
from entity.modalities import Modalities
from entity.pads import Pads
from entity.programs import Programs
from entity.persons import Persons
from entity.capacity_assessments import CapacityAssessments as CapacityAssessmentsEntity
from entity.capacity_assessments_states import CapacityAssessmentsStates as CapacityAssessmentsStatesEntity

from services import CapacityAssessments 
from services import SolicitudesAprobacionService
from dto.CapacityAssessmentsDTO import CapacityAssessmentListSP
from dto.AccionesSolicitudAprobacionCapacidadDTO import AccionSolicitudAprobacionCapacidad
from dto.AccionesSolicitudAprobacionDTO import AccionSolicitudAprobacion

CATEGORIA_APROBACION = "APP_EC"


router = APIRouter(
    prefix='/evaluaciones-de-capacidades',
    tags=['EvaluacionesDeCapacidades']
)


@router.get('')
def listar(db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    return CapacityAssessments.listar(db)

@router.get("/filtro")
def listar_capacity_assessments_filtro(
    db: DbSession,
    user_oid: str = Depends(get_current_user_oid),
    page: int = Query(...),
    estado: list[int] = Query([-1]),
    programa: Optional[int] = Query(-1),
    filtro: str = Query(""),
):
    try:
        return CapacityAssessments.listar_capacity_assessments_por_usuario_sp(
            db, user_oid, page, estado, filtro, programa
        )
        #return "me ve"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
     
  
@router.get("/filtro-test")
def listar_capacity_assessments_filtro_test(
    db: DbSession,
    guid: str = Depends(get_current_user_oid),
    page: int = Query(...),
    estado: list[int] = Query([-1]),
    programa: Optional[int] = Query(-1),
    filtro: str = Query(""),
):
    try:
        return CapacityAssessments.listar_capacity_assessments_por_usuario_sp(
            db, guid, page, estado, filtro, programa
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/{id}')
def obtener_por_id(id: int, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    pad = CapacityAssessments.obtener_por_id(id, db)
    if not pad:
        raise HTTPException(status_code=404, detail='evaluacion de capacidades  no encontrado')
    return pad


@router.post('', response_model=ResponseRequest)
def crear_programa(payload: CapacityAssessmentsCreate, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    try:      
        response_request = CapacityAssessments.crear(payload, db, user_oid)
        if response_request.solicitud_exitosa:
            return JSONResponse(
                content=response_request.model_dump(),
                status_code=status.HTTP_201_CREATED
            )
        if response_request.solicitud_exitosa==False:
                   return JSONResponse(
                       content=response_request.model_dump(),
                       status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
                   )       
    except HTTPException as e:
        print(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put('/{guid}', response_model=ResponseRequest)
def actualizar(guid: str, payload: CapacityAssessmentsCreate, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    try:
        evaluacion_db = CapacityAssessments.obtener_por_guid(guid, db)
        if not evaluacion_db:
            raise HTTPException(status_code=404, detail='Evaluación de capacidades no encontrada')
        response_request = CapacityAssessments.actualizar(evaluacion_db.id, payload, db)
        return JSONResponse(
            content=response_request.dict(),
            status_code=status.HTTP_200_OK if response_request.solicitud_exitosa else status.HTTP_400_BAD_REQUEST
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))   

@router.get('/{guid}/detalle')
def obtener_por_guid(guid: str, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    evaluacion = CapacityAssessments.obtener_por_guid(guid, db)
    if not evaluacion:
        raise HTTPException(status_code=404, detail='Evaluación de capacidades no encontrada')
    return evaluacion


@router.get('/{guid}/validar_acciones_aprobacion')
def validar_acciones_solicitud_aprobacion(guid: str, db: DbSession, user_oid: str = Depends(get_current_user_oid)):
    try:
        evaluacion = CapacityAssessments.obtener_por_guid(guid, db)
        if not evaluacion:
            raise HTTPException(status_code=404, detail='Evaluación de capacidades no encontrada')
        id_categoria = SolicitudesAprobacionService.obtener_categoria_aprobacion(CATEGORIA_APROBACION, db)
        respuesta = SolicitudesAprobacionService.validar_habilitar_acciones_solicitud_aprobacion(
            evaluacion.id, id_categoria, user_oid, db
        )
        return JSONResponse(content=respuesta.dict(), status_code=status.HTTP_200_OK)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





@router.post('/{guid}/accion_solicitud_aprobacion', response_model=ResponseRequest)
def accion_solicitud_aprobacion(
    guid: str,
    accion: AccionSolicitudAprobacionCapacidad,
    db: DbSession,
    user_oid: str = Depends(get_current_user_oid),
    
):
  
    try:
        
        evaluacion_db = CapacityAssessments.obtener_por_guid(guid, db)
        if not evaluacion_db:
            raise HTTPException(
                status_code=404,
                detail='Evaluación de capacidades no encontrada',
            )

        accion.id_evaluacion = evaluacion_db.id
        accion.id_solicitud_aprobacion = evaluacion_db.approval_request_id
        id_categoria = (
            SolicitudesAprobacionService.obtener_categoria_aprobacion(
                CATEGORIA_APROBACION, db
            )
        )

        respuesta = CapacityAssessments.procesar_accion_solicitud_aprobacion(
            accion, user_oid, id_categoria, db
        )

        return JSONResponse(
            content=respuesta.dict(),
            status_code=(
                status.HTTP_200_OK
                if respuesta.solicitud_exitosa
                else status.HTTP_400_BAD_REQUEST
            ),
        )
       
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
    
 
    
def generar_pdf_solicitud(evaluacion_db: CapacityAssessmentsEntity, db: DbSession) -> bytes:
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
    
    # PROGRAMA
    programa_name = "N/A"
    if evaluacion_db.program_id:
        program = db.query(Programs).filter(Programs.id == evaluacion_db.program_id).first()
        if program:
            programa_name = program.name

    #PAD
    pad_name = "N/A"
    if evaluacion_db.pid_id:
        pid = db.query(Pads).filter(Pads.id == evaluacion_db.pid_id).first()
        if pid:
            pad_name = pid.name
            
    #IMPLEMENTER
        implementer_name = "N/A"
        if evaluacion_db.implementer_id:
            implementer = db.query(Implementers).filter(Implementers.id == evaluacion_db.implementer_id).first()
            if implementer:
                implementer_name = implementer.acronym
         
    #MODALIDAD
        modalitie_name = "N/A"
        if evaluacion_db.modality_id:
            modalitie = db.query(Modalities).filter(Modalities.id == evaluacion_db.modality_id).first()
            if modalitie:
                modalitie_name = modalitie.name
    
    #ESTADO EVALUACION DE CAPACIDAD
        capacity_assessments_state_name = "N/A"
        if evaluacion_db.capacity_assessments_states_id:
            estado_evaluacion = db.query(CapacityAssessmentsStatesEntity).filter(CapacityAssessmentsStatesEntity.id == evaluacion_db.capacity_assessments_states_id).first()
            if estado_evaluacion:
                capacity_assessments_state_name = estado_evaluacion.state


    # RESPONSABLE
    
        responsable_name = "N/A"
        if evaluacion_db.persons_id:
            person = db.query(Persons).filter(Persons.id == evaluacion_db.persons_id).first()
            if person:
                 fullname= "{fname}  {lname} {olname}".format(fname = person.first_name, lname =person.last_name, olname =person.other_last_name)
                 responsable_name = fullname
    
       
    
    # FECHAS 
    start_date = evaluacion_db.start_date.strftime("%Y-%m-%d") if evaluacion_db.start_date else ""
    end_date = evaluacion_db.end_date.strftime("%Y-%m-%d") if evaluacion_db.end_date else ""
    policy_approval_date = evaluacion_db.policy_approval_date.strftime("%Y-%m-%d") if evaluacion_db.policy_approval_date else ""
    document_signature_date = evaluacion_db.document_signature_date.strftime("%Y-%m-%d") if evaluacion_db.document_signature_date else ""

   # VALOS
    approximate_value = f"{evaluacion_db.approximate_value:,.0f}" if evaluacion_db.approximate_value else ""
    
    # Logo local
    logo_path = Path(__file__).parent.parent.parent / "siva-ii-frontend" / "public" / "images" / "logos" / "logo_patrimonio.png"
    logo_uri = ""
    if logo_path.is_file():
        logo_uri = logo_path.as_uri()

    template_dir = Path(__file__).parent.parent / "templates"
    jinja_env = Environment(loader=FileSystemLoader(template_dir))
    template = jinja_env.get_template("evaluacion_capacidades.html")

    html_content = template.render(
        logo_path=logo_uri,
        name=evaluacion_db.name,
        code=evaluacion_db.code,
        programa=programa_name,
        pid=pad_name,
        modalidad=modalitie_name,
        implementer=implementer_name,
        person=responsable_name,
        capacity_assessments_state=capacity_assessments_state_name,
        observation=evaluacion_db.observation,
        start_date=start_date,
        end_date=end_date,
        policy_approval_date=policy_approval_date,
        document_signature_date=document_signature_date,
        approximate_value=approximate_value,
    )

    pdf_bytes = HTML(string=html_content).write_pdf()
    return pdf_bytes


@router.get("/{guid}/pdf_solicitud/documento")
def obtener_pdf_solicitud(guid: str, db: DbSession):
    try:
        evaluacion_db = db.query(CapacityAssessmentsEntity).filter(CapacityAssessmentsEntity.guid == guid).first()
        if not evaluacion_db:
            raise HTTPException(status_code=404, detail="Evaluación no encontrado")
            
        pdf_bytes = generar_pdf_solicitud(evaluacion_db, db)
        
        filename = f"solicitud_{evaluacion_db.name or evaluacion_db.CapacityAssessmentsEntity}.pdf"
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