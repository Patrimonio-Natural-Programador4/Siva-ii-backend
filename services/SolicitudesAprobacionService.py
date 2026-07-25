from datetime import date, datetime, datetime
import json

from dto.AccionesSolicitudAprobacionDTO import AccionesSolicitudAprobacionBase
from dto.ResponseRequest import ResponseRequest
from entity.approval_flow_steps import ApprovalFlowStep
from entity.users import Users
from entity.approval_request_history import ApprovalRequestHistory
from entity.approval_requests import ApprovalRequests
from entity.approval_role_users import ApprovalRoleUser
from entity.travel_requests import TravelRequests
from repository import ApprovalCategoryRepository, SolicitudesAprobacionRepository, UsuariosRepository
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, func
import logging
from dto.SolicitudAprobacionHistorialDTO import SolicitudAprobacionHistorialDTOBase
from entity.vw_approval_request_history import VWApprovalRequestHistory
from services import FlujosAprobacionService


ESTADO_APROBACION_ENVIADO = 2
ESTADO_APROBACION_AJUSTES = 3
ESTADO_APROBACION_APROBADO = 5
ESTADO_APROBACION_PENDIENTE = 6
ESTADO_APROBACION_FINALIZADO = 7

ESTADO_VIAJE_EN_APROBACION = 2
ESTADO_VIAJE_AJUSTES = 3
ESTADO_VIAJE_PENDIENTE_LEGALIZACION = 4

ALIAS_CATEGORIA_APROBACION = {
    "SV": "SOL_VIA_ANT",
}




def obtener_categoria_aprobacion(tipo_solicitud: str, db: Session) -> int:
    tipo_normalizado = ALIAS_CATEGORIA_APROBACION.get(tipo_solicitud, tipo_solicitud)
    category = ApprovalCategoryRepository.obtener_por_codigo(tipo_normalizado, db)
    if not category:
        raise Exception(f"Categoría de aprobación no encontrada para el tipo {tipo_solicitud}")
    return category.category_id    

def obtener_solicitud_aprobacion_por_id_asociado_id_categoria(id_registro_asociado: int, id_categoria: int, db: Session) -> list[SolicitudAprobacionHistorialDTOBase]:
    try:
        solicitudHistorial = (
            db.query(VWApprovalRequestHistory)
            .filter(
                VWApprovalRequestHistory.related_record_id == id_registro_asociado,
                VWApprovalRequestHistory.category_id == id_categoria
            )
            .order_by(
                asc(
                    func.coalesce(
                        VWApprovalRequestHistory.approved_at,
                        VWApprovalRequestHistory.created_at
                    )
                )
            )
            .all()
        )
        if len(solicitudHistorial) == 0:
            print(f"No se encontraron solicitudes de aprobación para el ID {id_registro_asociado} y categoría {id_categoria}.")
            return []

        # Convertir a DTO
        solicitudHistorialDTO = []
        for solicitud in solicitudHistorial:
            dto = SolicitudAprobacionHistorialDTOBase(
                id_historial=solicitud.history_id,
                id_solicitud_aprobacion=solicitud.approval_request_id,
                id_registro_asociado=solicitud.related_record_id,
                id_flujo_aprobacion=solicitud.approval_workflow_id,
                id_categoria=solicitud.category_id,
                id_estado_aprobacion_solicitud=solicitud.approval_status_id,
                id_rol_aprobacion=solicitud.approval_role_id,
                id_usuario=solicitud.user_id,
                id_estado_aprobacion_ruta=solicitud.approval_status_step_id,
                fecha_aprobacion=solicitud.approved_at if solicitud.approved_at else None,
                fecha_crea=solicitud.created_at if solicitud.created_at else None,
                observaciones=solicitud.comments,
                id_ruta=solicitud.step_id,
                orden=solicitud.step_order,
                # asigna_presupuesto_viajes=solicitud.asigna_presupuesto_viajes,
                # ajusta_itinerario_viajes=solicitud.ajusta_itinerario_viajes,
                rol=solicitud.rol,
                usuario=solicitud.user,
                categoria_aprobacion=solicitud.approval_category,
                guid=solicitud.guid,
                estado_aprobacion_ruta=solicitud.approval_route_status
            )
            solicitudHistorialDTO.append(dto)

        return solicitudHistorialDTO
    except Exception as e:
        logging.error(f"Error al obtener solicitud de aprobación: {e}")
        raise



def crear_solicitud_aprobacion(id_categoria_aprobacion: int, id_registro_asociado: int, id_usuario_solicita: int, 
                               codigo_instrumento: str, db: Session, id_supervisor: int = None, 
                               id_programa: int = None) -> int:
    try:

        numSolicitudes = SolicitudesAprobacionRepository.numero_solicitudes(db)
        fecha_actual = date.today()
        id_flujo_aprobacion, categoria, id_rol_aprobacion, id_ruta = FlujosAprobacionService.obtener_flujo_aprobacion_x_categoria_x_usuario_inicio_flujo(
            id_categoria_aprobacion, id_usuario_solicita, db, id_programa
        )
        
        if not id_flujo_aprobacion:
            print(f"No se encontró un flujo de aprobación para la categoría {id_categoria_aprobacion} y usuario {id_usuario_solicita}")
            print("No se encontró un flujo de aprobación válido.")

        nueva_solicitud = ApprovalRequests(
            approval_workflow_id = id_flujo_aprobacion,
            approval_status_id = 6,
            requester_user_id=id_usuario_solicita,
            name= f"Requerimiento de aprobación de {categoria}",
            code=f"SIVA-RA-{fecha_actual.year}-{numSolicitudes + 1}",
            created_date=datetime.now(),
            current_step=2,
            related_record_id=id_registro_asociado,
            instrument_code=codigo_instrumento
        )

        
        db.add(nueva_solicitud)
        db.commit()
        db.refresh(nueva_solicitud)
        asignar_inicio_ruta(
            nueva_solicitud.approval_request_id,
            id_rol_aprobacion,
            id_usuario_solicita,
            id_ruta,
            db
        )


        id_rol_aprobacion, id_ruta, es_supervisor = FlujosAprobacionService.obtener_siguiente_paso_ruta(
            id_categoria_aprobacion, 1, id_flujo_aprobacion,  db
        )

        # print("Validando siguiente paso en la cadena de aprobación...")
        # print(id_rol_aprobacion, id_ruta)

        asignar_siguiente_paso(
            nueva_solicitud.approval_request_id,
            id_rol_aprobacion,
            id_ruta,
            db,
            id_supervisor
        )


        return nueva_solicitud.approval_request_id
    except Exception as e:
        logging.error(f"Error al crear solicitud de aprobación: {e}")
        db.rollback()
        raise


def asignar_inicio_ruta(id_solicitud: int, id_rol_aprobacion: int, id_usuario: int, id_ruta: int, db: Session) -> None:
    try:
        solicitud_historial = ApprovalRequestHistory(
            approval_request_id=id_solicitud,
            approval_role_id=id_rol_aprobacion,
            user_id=id_usuario,
            approval_status_id=2,
            approved_at=datetime.now(),
            created_at=datetime.now(),
            received_at=datetime.now(),
            comments="Solicitud envíada para aprobación",
            step_id=id_ruta,
        )
        _asignar_usuario_aprobo_si_aplica(solicitud_historial, db)
        db.add(solicitud_historial)
        db.commit()

        # Lógica para asignar la ruta de inicio
        # ...

    except Exception as e:
        logging.error(f"Error al asignar inicio de ruta: {e}")
        db.rollback()


def _asignar_usuario_aprobo_si_aplica(historial: ApprovalRequestHistory, db: Session) -> None:
    if historial.approval_status_id != 6:
        historial.approved_by_user = _obtener_usuario_aprobo(historial.user_id, db)

def _obtener_usuario_aprobo(id_usuario: int, db: Session) -> str | None:
    if id_usuario is None:
        return None
    usuario = db.query(Users).filter(Users.id == id_usuario).first()
    if not usuario:
        return None
    return usuario.first_name + " " + usuario.other_name + " " + usuario.last_name + " " + usuario.other_last_name

def asignar_siguiente_paso(id_solicitud: int, id_rol_aprobacion: int, id_ruta: int, db: Session, id_supervisor: int = None) -> None:
    try:
        solicitud_historial = ApprovalRequestHistory(
            approval_request_id=id_solicitud,
            approval_role_id=id_rol_aprobacion,
            approval_status_id=6,
            created_at=datetime.now(),
            received_at=datetime.now(),
            comments=None,
            step_id=id_ruta,
            user_id=id_supervisor
        )
        _asignar_usuario_aprobo_si_aplica(solicitud_historial, db)
        db.add(solicitud_historial)
        db.commit()
    except Exception as e:
        logging.error(f"Error al asignar siguiente paso: {e}")
        db.rollback()


def _obtener_usuario_actual(user_oid: str, db: Session) -> Users:
    return UsuariosRepository.obtener_por_guid_msft(user_oid, db)


def _obtener_solicitud_por_registro_categoria(id_registro_asociado: int, db: Session) -> ApprovalRequests | None:
    return (
        db.query(ApprovalRequests)
        .filter(ApprovalRequests.related_record_id == id_registro_asociado)
        .order_by(desc(ApprovalRequests.approval_request_id))
        .first()
    )


def _obtener_paso_actual(solicitud: ApprovalRequests, db: Session) -> ApprovalFlowStep | None:
    if solicitud.current_step is None:
        return None
    return (
        db.query(ApprovalFlowStep)
        .filter(
            ApprovalFlowStep.approval_flow_id == solicitud.approval_workflow_id,
            ApprovalFlowStep.step_order == solicitud.current_step,
            ApprovalFlowStep.active == True,
        )
        .first()
    )


def _obtener_historial_pendiente(solicitud: ApprovalRequests, paso_actual: ApprovalFlowStep | None, db: Session) -> ApprovalRequestHistory | None:
    query = db.query(ApprovalRequestHistory).filter(
        ApprovalRequestHistory.approval_request_id == solicitud.approval_request_id,
        ApprovalRequestHistory.approval_status_id == ESTADO_APROBACION_PENDIENTE,
    )
    if paso_actual is not None:
        query = query.filter(ApprovalRequestHistory.step_id == paso_actual.step_id)
    return query.order_by(desc(ApprovalRequestHistory.history_id)).first()


def _usuario_puede_actuar(usuario_actual: Users, paso_actual: ApprovalFlowStep | None, historial_pendiente: ApprovalRequestHistory | None, db: Session) -> bool:
    if paso_actual is None:
        return False
    if historial_pendiente and historial_pendiente.user_id and historial_pendiente.user_id != usuario_actual.id:
        return False
    return (
        db.query(ApprovalRoleUser)
        .filter(
            ApprovalRoleUser.approval_role_id == paso_actual.approval_role_id,
            ApprovalRoleUser.user_id == usuario_actual.id,
            ApprovalRoleUser.active == True,
        )
        .first()
        is not None
    )


def _obtener_usuarios_disponibles_ajuste(solicitud: ApprovalRequests, db: Session) -> list[dict]:
    if solicitud.current_step is None or solicitud.current_step <= 1:
        return []

    historial = (
        db.query(VWApprovalRequestHistory)
        .filter(
            VWApprovalRequestHistory.approval_request_id == solicitud.approval_request_id,
            VWApprovalRequestHistory.step_order < solicitud.current_step,
            VWApprovalRequestHistory.user_id.is_not(None),
        )
        .order_by(VWApprovalRequestHistory.step_order.asc(), VWApprovalRequestHistory.history_id.asc())
        .all()
    )

    usuarios: list[dict] = []
    vistos: set[tuple[int | None, int | None]] = set()
    for item in historial:
        llave = (item.approval_role_id, item.user_id)
        if llave in vistos:
            continue
        vistos.add(llave)
        usuarios.append({
            "id_rol_aprobacion_ajuste": item.approval_role_id,
            "usuario": item.user,
            "id_usuario_ajuste": item.user_id,
        })
    return usuarios


def validar_habilitar_acciones_solicitud_aprobacion(id_registro_asociado: int, id_categoria: int, user_oid: str, db: Session, guid_solicitante = None) -> ResponseRequest:
    solicitud = _obtener_solicitud_por_registro_categoria(id_registro_asociado, db)
    if not solicitud:
        return ResponseRequest(solicitud_exitosa=False, mensaje="{}")

    usuario_actual = _obtener_usuario_actual(user_oid, db)
    paso_actual = _obtener_paso_actual(solicitud, db)
    historial_pendiente = _obtener_historial_pendiente(solicitud, paso_actual, db)
    usuarios_disponibles_ajustes = _obtener_usuarios_disponibles_ajuste(solicitud, db)
    puede_actuar = _usuario_puede_actuar(usuario_actual, paso_actual, historial_pendiente, db)

    acciones = {
        "id_solicitud_aprobacion": solicitud.approval_request_id,
        "asigna_presupuesto_viajes": paso_actual.assign_travel_budget if paso_actual else False,
        "ajusta_itinerario_viajes": paso_actual.adjust_travel_itinerary if paso_actual else False,
        "valida_soportes": paso_actual.validate_supporting_documents if paso_actual else False,
        "valida_soportes_hotel": paso_actual.validate_hotel_documents if paso_actual else False,
        "deshabilita_conceptos_anticipo": paso_actual.disable_advance_concepts if paso_actual else False,
        "agrega_rpc": paso_actual.add_rpc if paso_actual else False,
        "agrega_documento_contable": paso_actual.add_accounting_document if paso_actual else False,
        "agrega_tarjeta_asistencia_medica": paso_actual.add_medical_assistance_card if paso_actual else False,
        "agrega_comprobante_egreso": paso_actual.add_expense_voucher if paso_actual else False,
        "habilitar_pago": paso_actual.enable_payment if paso_actual else False,
        "orden_actual": solicitud.current_step,
        "id_estado_aprobacion_ruta": historial_pendiente.approval_status_id if historial_pendiente else None,
        "usuarios_disponibles_ajustes": usuarios_disponibles_ajustes,
        "usuario_solicito": str(guid_solicitante) == str(user_oid) if guid_solicitante else False,
        "habilitar_solicitar_ajustes": len(usuarios_disponibles_ajustes) > 0,
        "id_estado_solicitud": solicitud.approval_status_id,
    }

    return ResponseRequest(
        solicitud_exitosa=puede_actuar,
        mensaje=json.dumps(acciones),
        identity=solicitud.approval_request_id,
    )


def _marcar_historial_resuelto(historial: ApprovalRequestHistory, estado_aprobacion: int, usuario_actual: Users, comentarios: str | None, db: Session) -> None:
    historial.approval_status_id = estado_aprobacion
    historial.comments = comentarios if comentarios is not None else historial.comments
    historial.approved_at = datetime.now()
    historial.approver_user_id = usuario_actual.id
    historial.approved_by_user = _obtener_usuario_aprobo(usuario_actual.id, db)
    historial.user_id = usuario_actual.id


def _resolver_destino_ajuste(solicitud: ApprovalRequests, accion: AccionesSolicitudAprobacionBase, db: Session) -> tuple[ApprovalFlowStep | None, int | None, int | None]:
    usuarios_disponibles = _obtener_usuarios_disponibles_ajuste(solicitud, db)
    id_rol = accion.id_rol_aprobacion_ajuste or (usuarios_disponibles[0]["id_rol_aprobacion_ajuste"] if usuarios_disponibles else None)
    id_usuario = accion.id_usuario_ajuste if accion.id_usuario_ajuste is not None else (usuarios_disponibles[0]["id_usuario_ajuste"] if usuarios_disponibles else None)
    if id_rol is None:
        return None, None, None

    paso = (
        db.query(ApprovalFlowStep)
        .filter(
            ApprovalFlowStep.approval_flow_id == solicitud.approval_workflow_id,
            ApprovalFlowStep.approval_role_id == id_rol,
            ApprovalFlowStep.step_order < (solicitud.current_step or 0),
            ApprovalFlowStep.active == True,
        )
        .order_by(desc(ApprovalFlowStep.step_order))
        .first()
    )
    return paso, id_rol, id_usuario


def ejecutar_accion_solicitud_aprobacion(viaje: TravelRequests, accion: AccionesSolicitudAprobacionBase, id_categoria: int, user_oid: str, db: Session) -> ResponseRequest:
    solicitud = _obtener_solicitud_por_registro_categoria(viaje.travel_request_id, db)
    if not solicitud:
        return ResponseRequest(solicitud_exitosa=False, mensaje="No se encontró una solicitud de aprobación activa")

    usuario_actual = _obtener_usuario_actual(user_oid, db)
    paso_actual = _obtener_paso_actual(solicitud, db)
    historial_pendiente = _obtener_historial_pendiente(solicitud, paso_actual, db)

    if historial_pendiente is None or paso_actual is None:
        return ResponseRequest(solicitud_exitosa=False, mensaje="No se encontró el paso pendiente de aprobación")

    if not _usuario_puede_actuar(usuario_actual, paso_actual, historial_pendiente, db):
        return ResponseRequest(solicitud_exitosa=False, mensaje="El usuario actual no tiene permisos para ejecutar esta acción")

    tipo_accion = (accion.tipo_accion or "").upper().strip()
    comentarios = (accion.comentarios or "").strip() or None

    if tipo_accion == "APROBAR":
        _marcar_historial_resuelto(historial_pendiente, ESTADO_APROBACION_APROBADO, usuario_actual, comentarios, db)
        siguiente_rol, siguiente_ruta, es_supervisor = FlujosAprobacionService.obtener_siguiente_paso_ruta(
            id_categoria,
            solicitud.current_step or 0,
            solicitud.approval_workflow_id,
            db,
        )
        if siguiente_rol and siguiente_ruta:
            solicitud.current_step = (solicitud.current_step or 0) + 1
            solicitud.approval_status_id = ESTADO_APROBACION_PENDIENTE
            viaje.travel_status_id = ESTADO_VIAJE_EN_APROBACION
            viaje.current_request_order = solicitud.current_step
            asignar_siguiente_paso(
                solicitud.approval_request_id,
                siguiente_rol,
                siguiente_ruta,
                db,
                viaje.supervisor_user_id if es_supervisor else None,
            )
        else:
            historial_pendiente.approval_status_id = ESTADO_APROBACION_FINALIZADO
            solicitud.approval_status_id = ESTADO_APROBACION_FINALIZADO
            viaje.travel_status_id = ESTADO_VIAJE_PENDIENTE_LEGALIZACION
            viaje.current_request_order = solicitud.current_step
        db.commit()
        return ResponseRequest(solicitud_exitosa=True, mensaje="Solicitud aprobada correctamente", identity=solicitud.approval_request_id)

    if tipo_accion == "AJUSTAR":
        paso_ajuste, id_rol_ajuste, id_usuario_ajuste = _resolver_destino_ajuste(solicitud, accion, db)
        if paso_ajuste is None or id_rol_ajuste is None:
            return ResponseRequest(solicitud_exitosa=False, mensaje="No se encontró un destino válido para solicitar ajustes")

        _marcar_historial_resuelto(historial_pendiente, ESTADO_APROBACION_AJUSTES, usuario_actual, comentarios, db)
        solicitud.approval_status_id = ESTADO_APROBACION_AJUSTES
        solicitud.current_step = paso_ajuste.step_order
        viaje.travel_status_id = ESTADO_VIAJE_AJUSTES
        viaje.current_request_order = paso_ajuste.step_order
        db.add(ApprovalRequestHistory(
            approval_request_id=solicitud.approval_request_id,
            approval_role_id=id_rol_ajuste,
            approval_status_id=ESTADO_APROBACION_PENDIENTE,
            created_at=datetime.now(),
            received_at=datetime.now(),
            comments=None,
            step_id=paso_ajuste.step_id,
            user_id=id_usuario_ajuste,
        ))
        db.commit()
        return ResponseRequest(solicitud_exitosa=True, mensaje="Ajustes solicitados correctamente", identity=solicitud.approval_request_id)

    return ResponseRequest(solicitud_exitosa=False, mensaje="La acción solicitada no es válida")

