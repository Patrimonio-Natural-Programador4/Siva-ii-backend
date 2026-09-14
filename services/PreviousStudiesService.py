#SERVICE ESTUDIOS PREVIOS

import logging
import uuid
from datetime import datetime, date
from sqlalchemy.orm import Session

from dto.AccionesSolicitudAprobacionCapacidadDTO import AccionSolicitudAprobacionCapacidad
from dto.AccionesSolicitudAprobacionDTO import AccionSolicitudAprobacion
from dto.PreviousStudiesDTO import PreviousStudiesBase, PreviousStudiesCreate, PreviousStudiesListDTO
from dto.ResponseRequest import ResponseRequest
from entity.implementers import Implementers
from entity.previous_studies import PreviousStudies as PreviousStudiesEntity 
from exceptions import PruebaNotFoundError
from repository import PreviousStudiesRepository, UsuariosRepository
from services import PreviousStudiesService
from services import SolicitudesAprobacionService


CATEGORIA_APROBACION_previous_studies = "APP_EP"  #APP_EP
ID_ESTADO_REVISION = 2   # Revisión
ID_ESTADO_AJUSTES = 3   # Solicitud de ajustes
ID_ESTADO_APROBADO = 5  # Aprobado


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
            previous_studies_states_id=e.previous_studies_states_id,
            prev_studies_state=e.prev_studies_state.state if e.prev_studies_state else None,
            approval_request_id=e.approval_request_id,
            guid=e.guid,                                          # <-- agregado
            app_request=e.app_request.name if e.app_request else None,
            implementer_id=e.implementer_id,
            implementers=e.implementers.acronym if (e.implementers and hasattr(e.implementers, 'acronym')) else None,
            persons_id=e.persons_id,
            persons=(
                " ".join(p for p in [e.persons.first_name, e.persons.other_name, e.persons.last_name, e.persons.other_last_name] if p)
                if e.persons else None
            ),
            capacity_assessment_id=e.capacity_assessment_id,
            capacity_assessment=e.capacity_assessment.name if e.capacity_assessment else None,
            program_id=e.program_id,
            programs =e.programs.description if e.programs else None,
            code =e.code 
            
        )
        for e in estudios
    ]
    
def obtener_est_previo_por_id(id: int, db: Session) -> PreviousStudiesBase | None:
    e = PreviousStudiesRepository.obtener_por_id(id, db)
    if not e:
        return None
    return PreviousStudiesBase(
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
            previous_studies_states_id=e.previous_studies_states_id,
            prev_studies_state=e.prev_studies_state.state if e.prev_studies_state else None,
            approval_request_id=e.approval_request_id,
            guid=e.guid,                                          # <-- agregado
            app_request=e.app_request.name if e.app_request else None,
            implementer_id=e.implementer_id,
            implementers=e.implementers.acronym if (e.implementers and hasattr(e.implementers, 'acronym')) else None,
            persons_id=e.persons_id,
            persons=(
                " ".join(p for p in [e.persons.first_name, e.persons.other_name, e.persons.last_name, e.persons.other_last_name] if p)
                if e.persons else None
            ),
            capacity_assessment_id=e.capacity_assessment_id,
            capacity_assessment=e.capacity_assessment.name if e.capacity_assessment else None,
            program_id=e.program_id,
            programs =e.programs.description if e.programs else None,
            code =e.code 
                            
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
        nuevo_estudio_previo.previous_studies_states_id= previous_studies.previous_studies_states_id
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
            id_programa=nuevo_estudio_previo.program_id 
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
        


def obtener_por_guid(guid: str, db: Session) -> PreviousStudiesBase | None:
    e = PreviousStudiesRepository.obtener_por_guid(guid, db)
    if not e:
        return None
    return PreviousStudiesBase(
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
       previous_studies_states_id=e.previous_studies_states_id,
       prev_studies_state=e.prev_studies_state.state if e.prev_studies_state else None,
       approval_request_id=e.approval_request_id,
       guid=e.guid,
       app_request=e.app_request.name if e.app_request else None,
       implementer_id=e.implementer_id,
       implementers=e.implementers.acronym if (e.implementers and hasattr(e.implementers, 'acronym')) else None,
       persons_id=e.persons_id,
       persons=(
                " ".join(p for p in [e.persons.first_name, e.persons.other_name, e.persons.last_name, e.persons.other_last_name] if p)
                if e.persons else None
            ),
       capacity_assessment_id=e.capacity_assessment_id,
       capacity_assessment=e.capacity_assessment.name if e.capacity_assessment else None,
       program_id=e.program_id,
       programs =e.programs.description if e.programs else None,
       code =e.code
    )
    
def listar_previous_studies_por_usuario_sp(
    db: Session,
    usuario_guid: str,
    page: int,
    estado: list[int],
    filtro: str,
    programa: int,
) -> list[PreviousStudiesListDTO]:
    return PreviousStudiesRepository.listar_previous_studies_por_usuario_sp(
        usuario_guid, db, page, estado, filtro, programa
    )
    
def procesar_accion_solicitud_aprobacion(
    accion: AccionSolicitudAprobacion,
    usuario_guid: str,
    id_categoria: int,
    db: Session,
) -> ResponseRequest:
    try:
        usuario = UsuariosRepository.obtener_por_guid_msft(usuario_guid.strip(), db)
        if not usuario:
            raise PruebaNotFoundError("Usuario no encontrado")

        respuesta = SolicitudesAprobacionService.actualizar_ruta(
            accion, id_categoria, usuario.id, db,
            id_supervisor=None,
            identity=accion.estudio_previo.id
        )

        if respuesta.solicitud_exitosa:
            estudio_db = PreviousStudiesRepository.obtener_por_guid_id_solicitud_aprobacion(
                accion.estudio_previo.guid, accion.id_solicitud_aprobacion, db
            )
            if not estudio_db:
                raise PruebaNotFoundError("Estudio previo no encontrado")

            if respuesta.mensaje == "RUTA_COMPLETA":
                estudio_db.previous_studies_states_id = ID_ESTADO_APROBADO
            elif respuesta.mensaje == "EN_PROCESO":
                estudio_db.previous_studies_states_id = ID_ESTADO_REVISION
            elif respuesta.mensaje == "AJUSTES":
                estudio_db.previous_studies_states_id = ID_ESTADO_AJUSTES

            db.commit()

        return respuesta
    except Exception as e:
        logging.error(f"Error al procesar acción de aprobación de estudio previo: {e}")
        return ResponseRequest(solicitud_exitosa=False, mensaje=str(e))
    
    
    
def obtener_por_guid_id_solicitud_aprobacion(guid: str, id_solicitud_aprobacion: int, db: Session) -> PreviousStudiesEntity | None:
    try:
        return db.query(PreviousStudiesEntity).filter(
            PreviousStudiesEntity.guid == guid,
            PreviousStudiesEntity.approval_request_id == id_solicitud_aprobacion
        ).first()
    except Exception as e:
        logging.error(f"Failed to get PreviousStudies by guid and approval_request_id: {str(e)}")
        raise PruebaNotFoundError(str(e))    
    
    
def actualizar(id: int, payload: PreviousStudiesCreate, db: Session) -> ResponseRequest:
    try:
        registro = PreviousStudiesRepository.obtener_por_id(id, db)
        if not registro:
            return ResponseRequest(solicitud_exitosa=False, mensaje='Estudio previo no encontrado')

        registro.precedents = payload.precedents
        registro.justification = payload.justification
        registro.scope = payload.scope
        registro.overall_objective = payload.overall_objective
        registro.term = payload.term
        registro.obligations = payload.obligations
        registro.supervisor = payload.supervisor
        registro.total_value = payload.total_value
        registro.contributions_ei = payload.contributions_ei
        registro.total_value_executes_fpn = payload.total_value_executes_fpn
        registro.total_value_executes_ei = payload.total_value_executes_ei
        registro.previous_studies_states_id = payload.previous_studies_states_id
        registro.implementer_id = payload.implementer_id
        registro.persons_id = payload.persons_id
        registro.capacity_assessment_id = payload.capacity_assessment_id
        registro.contributions_fpn = payload.contributions_fpn
        registro.estimated_term = payload.estimated_term
        registro.program_id = payload.program_id

        db.commit()
        return ResponseRequest(solicitud_exitosa=True, mensaje='Estudio previo actualizado exitosamente', identity=registro.id)
    except Exception as e:
        db.rollback()
        logging.error(f"Error al actualizar estudio previo: {e}")
        return ResponseRequest(solicitud_exitosa=False, mensaje=str(e))