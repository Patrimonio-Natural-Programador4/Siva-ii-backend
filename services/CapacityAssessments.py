import logging
from datetime import datetime, date
from sqlalchemy.orm import Session

from dto.CapacityAssessmentsDTO import CapacityAssessmentsBase,CapacityAssessmentsCreate,CapacityAssessmentListSP
from dto.ResponseRequest import ResponseRequest
from entity.implementers import Implementers
from entity.capacity_assessments import CapacityAssessments as CapacityAssessmentsEntity  
from repository import CapacityAssessments  
from repository import UsuariosRepository
from services import SolicitudesAprobacionService
from repository import CapacityAssessments  as repo
from exceptions import PruebaCreationError, PruebaNotFoundError
from dto.AccionesSolicitudAprobacionCapacidadDTO import AccionSolicitudAprobacionCapacidad

CATEGORIA_APROBACION_CAPACITY_ASSESSMENT = "APP_EC"
ID_ESTADO_ENVIADO = 2   # Revisión
ID_ESTADO_AJUSTES = 3   # Solicitud de ajustes
ID_ESTADO_APROBADO = 5  # Aprobado


def listar(db: Session) -> list[CapacityAssessmentsBase]:
    capacidades = CapacityAssessments.listar(db)
    return [
        CapacityAssessmentsBase(
            id=int(c.id),
            name=c.name,
            observation=c.observation,
            approximate_value=c.approximate_value,
            guid=c.guid,
            user_session=c.user_session,
            create_date=c.create_date,
            policy_approval_date=c.policy_approval_date,
            end_date=c.end_date,
            start_date=c.start_date,
            codigo= c.code,
            
            document_signature_date=c.document_signature_date,
            capacity_assessments_state=c.capacity_assessments_state.state if c.capacity_assessments_state else None,
            implementer=c.implementer.acronym if c.implementer else None,
            modalitie=c.modalitie.name if c.modalitie else None,
            person=c.person.email if c.person else None,
            pid=c.pid.name if c.pid else None,
            programa=c.programa.name if c.programa else None,
            aproval_request=c.approval_request.name if c.approval_request else None,
            approval_request_id=c.approval_request_id,   
            program_id=c.program_id,
            pid_id=c.pid_id,
            implementer_id=c.implementer_id,
            persons_id=c.persons_id,
            capacity_assessments_states_id=c.capacity_assessments_states_id,
            modality_id=c.modality_id,
        )
        for c in capacidades
    ]

def obtener_por_id(id: int, db: Session) -> CapacityAssessmentsBase | None:
    c = CapacityAssessments.obtener_por_id(id, db)
    if not c:
        return None
    return CapacityAssessmentsBase(
                id=int(c.id),
                name=c.name,
                observation=c.observation,
                approximate_value=c.approximate_value,
                guid=c.guid,
                user_session=c.user_session,
                create_date=c.create_date,
                policy_approval_date=c.policy_approval_date,
                end_date=c.end_date,
                start_date=c.start_date,
                codigo= c.code,
                document_signature_date=c.document_signature_date,
                capacity_assessments_state=c.capacity_assessments_state.state ,
                implementer=c.implementer.acronym ,
                modalitie=c.modalitie.name ,
                person=c.person.email  ,
                pid=c.pid.name ,
                programa=c.programa.name ,
                program_id=c.program_id,
                pid_id=c.pid_id,
                implementer_id=c.implementer_id,
                persons_id=c.persons_id,
                capacity_assessments_states_id=c.capacity_assessments_states_id,
                modality_id=c.modality_id,
                approval_request_id=c.approval_request_id,   
            )

def crear(capacity_assessment: CapacityAssessmentsCreate, db: Session, usuario_guid: str) -> ResponseRequest:
    respuesta = ResponseRequest(solicitud_exitosa=True)
    try:
        usuario = UsuariosRepository.obtener_por_guid_msft(usuario_guid.strip(), db)
        print('usuario',usuario)
        if not usuario:
            raise Exception("Usuario no encontrado")       
        existe_capacidad = CapacityAssessments.obtener_por_nombre(capacity_assessment.name or '', db)
        if existe_capacidad:
            return ResponseRequest(mensaje='Ya existe una evaluación de capacidad con ese nombre', solicitud_exitosa=False)

        nueva_capacidad = CapacityAssessmentsEntity()  
        nueva_capacidad.name = capacity_assessment.name
        nueva_capacidad.code = capacity_assessment.code
        nueva_capacidad.observation = capacity_assessment.observation
        nueva_capacidad.approximate_value = capacity_assessment.approximate_value
        nueva_capacidad.user_session = usuario.id
        nueva_capacidad.create_date = datetime.now()
        nueva_capacidad.policy_approval_date = capacity_assessment.policy_approval_date
        nueva_capacidad.document_signature_date = capacity_assessment.document_signature_date
        nueva_capacidad.start_date = capacity_assessment.start_date
        nueva_capacidad.end_date = capacity_assessment.end_date
        nueva_capacidad.program_id = capacity_assessment.program_id
        nueva_capacidad.pid_id = capacity_assessment.pid_id
        nueva_capacidad.implementer_id = capacity_assessment.implementer_id
        nueva_capacidad.persons_id = capacity_assessment.persons_id
        nueva_capacidad.capacity_assessments_states_id = capacity_assessment.capacity_assessments_states_id
        nueva_capacidad.modality_id = capacity_assessment.modality_id
        nueva_capacidad.approval_request_id = capacity_assessment.approval_request_id

        print('usuario', capacity_assessment.user_session)
        db.add(nueva_capacidad)
        db.commit()
        db.refresh(nueva_capacidad)

        id_categoria_aprobacion = SolicitudesAprobacionService.obtener_categoria_aprobacion(
            CATEGORIA_APROBACION_CAPACITY_ASSESSMENT, db
        )
        if not id_categoria_aprobacion:
            raise Exception(
                f"No se encontró la categoría de aprobación con el código {CATEGORIA_APROBACION_CAPACITY_ASSESSMENT}"
            )

        id_solicitud_aprobacion = SolicitudesAprobacionService.crear_solicitud_aprobacion(
            id_categoria_aprobacion,
            nueva_capacidad.id,
            usuario.id,
            nueva_capacidad.guid,
            db,
            id_programa=capacity_assessment.program_id
        )

        nueva_capacidad.approval_request_id = id_solicitud_aprobacion
        db.commit()
        db.refresh(nueva_capacidad)

        respuesta.identity = nueva_capacidad.id
        respuesta.mensaje = "Evaluación de capacidades creado exitosamente"
        return respuesta

    except Exception as e:
        logging.error(f"Error al crear evaluación de capacidades: {e}")
        print('el error es:', e)
        db.rollback()
        return ResponseRequest(
            solicitud_exitosa=False,
            mensaje=str(e)
        )
        
        
def obtener_por_guid(guid: str, db: Session) -> CapacityAssessmentsBase | None:
    c = CapacityAssessments.obtener_por_guid(guid, db)
    if not c:
        return None
    return CapacityAssessmentsBase(
        id=int(c.id),
        name=c.name,
        observation=c.observation,
        approximate_value=c.approximate_value,
        guid=c.guid,
        user_session=c.user_session,
        create_date=c.create_date,
        policy_approval_date=c.policy_approval_date,
        end_date=c.end_date,
        start_date=c.start_date,
        codigo=c.code,
        document_signature_date=c.document_signature_date,
        capacity_assessments_state=c.capacity_assessments_state.state if c.capacity_assessments_state else None,
        implementer=c.implementer.acronym if c.implementer else None,
        modalitie=c.modalitie.name if c.modalitie else None,
        person=c.person.email if c.person else None,
        pid=c.pid.name if c.pid else None,
        programa=c.programa.name if c.programa else None,
        aproval_request=c.approval_request.name if c.approval_request else None,
        approval_request_id=c.approval_request_id,   
        program_id=c.program_id,
        pid_id=c.pid_id,
        implementer_id=c.implementer_id,
        persons_id=c.persons_id,
        capacity_assessments_states_id=c.capacity_assessments_states_id,
        modality_id=c.modality_id,
    )    
    

def listar_capacity_assessments_por_usuario_sp(
    db: Session,
    usuario_guid: str,
    page: int,
    estado: list[int],
    filtro: str,
    programa: int = -1,
) -> list[CapacityAssessmentListSP]:
    try:
        return repo.listar_capacity_assessments_por_usuario_sp(
            usuario_guid, db, page, estado, filtro, programa
        )
    except Exception as e:
        logging.error(f"Failed to list capacity assessments: {str(e)}")
        raise PruebaNotFoundError(str(e))    
    
    


def procesar_accion_solicitud_aprobacion(
    accion: AccionSolicitudAprobacionCapacidad,
    usuario_guid: str,
    id_categoria: int,
    db: Session,
) -> ResponseRequest:
    try:
        usuario = UsuariosRepository.obtener_por_guid_msft(usuario_guid.strip(), db)
        if not usuario:
            print('Usuario no encontrado')
            raise Exception("Usuario no encontrado")

        respuesta = SolicitudesAprobacionService.actualizar_ruta(
            accion, id_categoria, usuario.id, db,
            id_supervisor=None, identity=accion.id_evaluacion
        )

        if respuesta.solicitud_exitosa:
            evaluacion_db = CapacityAssessments.obtener_por_id(accion.id_evaluacion, db)
            if respuesta.mensaje == "RUTA_COMPLETA":
                evaluacion_db.capacity_assessments_states_id = ID_ESTADO_APROBADO
            elif respuesta.mensaje == "EN_PROCESO":
                evaluacion_db.capacity_assessments_states_id = ID_ESTADO_ENVIADO
            elif respuesta.mensaje == "AJUSTES":
                evaluacion_db.capacity_assessments_states_id = ID_ESTADO_AJUSTES
            db.commit()

        return respuesta
    except Exception as e:
        logging.error(f"Error al procesar acción de aprobación: {e}")
        return ResponseRequest(solicitud_exitosa=False, mensaje=str(e))
    
    
    
def actualizar(id: int, payload: CapacityAssessmentsCreate, db: Session) -> ResponseRequest:
    try:
        registro = CapacityAssessments.obtener_por_id(id, db)
        if not registro:
            return ResponseRequest(solicitud_exitosa=False, mensaje='Evaluación no encontrada')

        registro.name = payload.name
        registro.code = payload.code
        registro.observation = payload.observation
        registro.approximate_value = payload.approximate_value
        registro.policy_approval_date = payload.policy_approval_date
        registro.document_signature_date = payload.document_signature_date
        registro.start_date = payload.start_date
        registro.end_date = payload.end_date
        registro.program_id = payload.program_id
        registro.pid_id = payload.pid_id
        registro.implementer_id = payload.implementer_id
        registro.persons_id = payload.persons_id
        registro.capacity_assessments_states_id = payload.capacity_assessments_states_id
        registro.modality_id = payload.modality_id

        db.commit()
        return ResponseRequest(solicitud_exitosa=True, mensaje='Evaluación actualizada exitosamente', identity=registro.id)
    except Exception as e:
        db.rollback()
        logging.error(f"Error al actualizar capacity assessment: {e}")
        return ResponseRequest(solicitud_exitosa=False, mensaje=str(e))    