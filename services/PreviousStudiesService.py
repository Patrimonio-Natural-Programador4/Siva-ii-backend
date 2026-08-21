#SERVICE ESTUDIOS PREVIOS

import logging
import uuid
from datetime import datetime, date
from sqlalchemy.orm import Session

from dto.PreviousStudiesDTO import PreviousStudiesBase, PreviousStudiesCreate
from dto.ResponseRequest import ResponseRequest
from entity.implementers import Implementers
from entity.previous_studies import PreviousStudies as PreviousStudiesEntity 
from repository import PreviousStudiesRepository, UsuariosRepository
from services import PreviousStudiesService
from services import SolicitudesAprobacionService


CATEGORIA_APROBACION_previous_studies = "APP_EP"  #APP_EP
def listar(db: Session) -> list[PreviousStudiesBase]:
    estudios = PreviousStudiesRepository.listar(db)
    return [
       PreviousStudiesBase(
            id=int(e.id),
            precedents=e.precedents,
            justification=e.justification,
            scope=e.scope,
            overall_objective=e.overall_objective,
            term=e.term,
            obligations= e.obligations,
            supervisor = e.supervisor,
            user_session=e.user_session,
            create_date=e.create_date,
            total_value= e.total_value,
            contributions_ei= e.contributions_ei,
            total_value_executes_fpn=e.total_value_executes_fpn,
            total_value_executes_ei= e.total_value_executes_ei,
            contributions_fpn = e.contributions_fpn,
            estimated_term=e.estimated_term,           
            cap_assessments_state=e.cap_assessments_state.state if e.cap_assessments_state else None,
            app_request=e.app_request.name if e.app_request else None,
            implementers=e.implementers.acronym if (e.implementers and hasattr(e.implementers, 'acronym')) else None,
            persons=e.persons.email if e.persons else None,
            capacity_assessment=e.capacity_assessment.name if e.capacity_assessment else None,
            programs =e.programs.description if e.programs else None,
            code =e.code 
            
        )
        for e in estudios
    ]
    
def obtener_est_previo_por_id(id: int, db: Session) -> PreviousStudiesBase | None:
    c = PreviousStudiesRepository.obtener_por_id(id, db)
    if not c:
        return None
    return PreviousStudiesBase(
                id=int(c.id),
                precedents=c.precedents,
                justification=c.justification,
                scope=c.scope,
                overall_objective=c.overall_objective,
                term=c.term,
                obligations= c.obligations,
                supervisor = c.supervisor,
                user_session=c.user_session,
                create_date=c.create_date,
                total_value= c.total_value,
                contributions_ei= c.contributions_ei,
                total_value_executes_fpn=c.total_value_executes_fpn,
                total_value_executes_ei= c.total_value_executes_ei,
                contributions_fpn = c.contributions_fpn,
                estimated_term=c.estimated_term,           
                cap_assessments_state=c.cap_assessments_state.state if c.cap_assessments_state else None,
                app_request=c.app_request.name if c.app_request else None,
                implementers=c.implementers.acronym if (c.implementers and hasattr(c.implementers, 'acronym')) else None,
                persons=c.persons.email if c.persons else None,
                capacity_assessment=c.capacity_assessment.name if c.capacity_assessment else None,
                programs =c.programs.description if c.programs else None,
                code= c.code
            )   
    


def crearEstudioPrevio(previous_studies: PreviousStudiesCreate, db: Session, usuario_guid: str) -> ResponseRequest:
    respuesta = ResponseRequest(solicitud_exitosa=True)
    try:
        usuario = UsuariosRepository.obtener_por_guid_msft(usuario_guid.strip(), db)
        if not usuario:
            raise Exception("Usuario no encontrado")
        fecha_actual = date.today()
        estudios_previos=PreviousStudiesRepository.numero_estudios_previos(db)
        
        nuevo_estudio_previo = PreviousStudiesEntity()  
        nuevo_estudio_previo.precedents = previous_studies.precedents
        nuevo_estudio_previo.justification = previous_studies.justification
        nuevo_estudio_previo.scope = previous_studies.scope
        nuevo_estudio_previo.overall_objective = previous_studies.overall_objective
        nuevo_estudio_previo.term = previous_studies.term
        nuevo_estudio_previo.obligations = previous_studies.obligations
        nuevo_estudio_previo.supervisor = previous_studies.supervisor
        nuevo_estudio_previo.user_session = previous_studies.user_session
        nuevo_estudio_previo.create_date = datetime.now().replace(tzinfo=None)
        nuevo_estudio_previo.total_value = previous_studies.total_value
        nuevo_estudio_previo.contributions_ei = previous_studies.contributions_ei
        nuevo_estudio_previo.total_value_executes_fpn = previous_studies.total_value_executes_fpn
        nuevo_estudio_previo.total_value_executes_ei = previous_studies.total_value_executes_ei
        nuevo_estudio_previo.capacity_assessments_states_id = previous_studies.capacity_assessments_states_id
        nuevo_estudio_previo.approval_request_id = previous_studies.approval_request_id
        nuevo_estudio_previo.implementer_id = previous_studies.implementer_id
        nuevo_estudio_previo.persons_id = previous_studies.persons_id
        nuevo_estudio_previo.capacity_assessment_id = previous_studies.capacity_assessment_id
        nuevo_estudio_previo.contributions_fpn = previous_studies.contributions_fpn
        nuevo_estudio_previo.estimated_term = previous_studies.estimated_term
        nuevo_estudio_previo.program_id = previous_studies.program_id
        nuevo_estudio_previo.code = f"EP-{fecha_actual.year}-{estudios_previos+1:02d}"

        db.add(nuevo_estudio_previo)
        db.commit()
        db.refresh(nuevo_estudio_previo)

        id_categoria_aprobacion = SolicitudesAprobacionService.obtener_categoria_aprobacion(
            CATEGORIA_APROBACION_previous_studies, db
        )
        if not id_categoria_aprobacion:
            raise Exception(
                f"No se encontró la categoría de aprobación con el código {CATEGORIA_APROBACION_previous_studies}"
            )

        id_solicitud_aprobacion = SolicitudesAprobacionService.crear_solicitud_aprobacion(
            id_categoria_aprobacion,
            nuevo_estudio_previo.id,
            usuario.id,
            nuevo_estudio_previo.code, #code 
            db,
            nuevo_estudio_previo.program_id 
        )

        nuevo_estudio_previo.approval_request_id = id_solicitud_aprobacion
        db.commit()
        db.refresh(nuevo_estudio_previo)

        respuesta.identity = nuevo_estudio_previo.id
        respuesta.mensaje = "Estudio previo creado exitosamente"
        return respuesta

    except Exception as e:
        logging.error(f"Error al crear estudio previo: {e}")
        print('el error es:', e)
        db.rollback()
        return ResponseRequest(
            solicitud_exitosa=False,
            mensaje=str(e)
        )
        
