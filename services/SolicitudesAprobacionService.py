from datetime import date, datetime, datetime
import json

from dto.AccionesSolicitudAprobacionDTO import AccionSolicitudAprobacion, AccionSolicitudAprobacion
from dto.ResponseRequest import ResponseRequest
from entity.approval_flow_steps import ApprovalFlowStep
from entity.users import Users
from entity.approval_request_history import ApprovalRequestHistory
from entity.approval_requests import ApprovalRequests
from entity.approval_role_users import ApprovalRoleUser
from entity.travel_requests import TravelRequests
from repository import ApprovalCategoryRepository, ApprovalFlowRepository, ApprovalRequestHistoryRepository, ApprovalRequestsRepository, SolicitudesAprobacionRepository, UsuariosRepository
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, func
import logging
from dto.SolicitudAprobacionHistorialDTO import SolicitudAprobacionHistorialDTOBase
from entity.vw_approval_request_history import VWApprovalRequestHistory
from services import FlujosAprobacionService


ESTADO_APROBACION_ENVIADO = 2
ESTADO_APROBACION_AJUSTES = 3
ESTADO_APROBACION_NO_APROBADO = 4
ESTADO_APROBACION_APROBADO = 5
ESTADO_APROBACION_PENDIENTE = 6
ESTADO_APROBACION_FINALIZADO = 7
ESTADO_APROBACION_AJUSTES_REALIZADOS = 8

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
        solicitudHistorial = ApprovalRequestHistoryRepository.obtener_historial_por_registro_asociado_categoria(id_registro_asociado, id_categoria, db)
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
            approval_status_id = ESTADO_APROBACION_PENDIENTE,
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
            approval_status_id=ESTADO_APROBACION_ENVIADO,
            approved_at=datetime.now(),
            created_at=datetime.now(),
            received_at=datetime.now(),
            comments="Solicitud envíada para aprobación",
            step_id=id_ruta,
        )
        asignar_usuario_aprobo_si_aplica(solicitud_historial, db)
        db.add(solicitud_historial)
        db.commit()

        # Lógica para asignar la ruta de inicio
        # ...

    except Exception as e:
        logging.error(f"Error al asignar inicio de ruta: {e}")
        db.rollback()


def asignar_usuario_aprobo_si_aplica(historial: ApprovalRequestHistory, db: Session) -> None:
    if historial.approval_status_id != ESTADO_APROBACION_PENDIENTE:
        historial.approved_by_user = obtener_usuario_aprobo(historial.user_id, db)

def obtener_usuario_aprobo(id_usuario: int, db: Session) -> str | None:
    if id_usuario is None:
        return None
    usuario = UsuariosRepository.obtener_usuario_por_id([id_usuario], db)
    usuario = usuario[0] if usuario else None
    if not usuario:
        return None
    return usuario.first_name + " " + usuario.other_name + " " + usuario.last_name + " " + usuario.other_last_name

def asignar_siguiente_paso(id_solicitud: int, id_rol_aprobacion: int, id_ruta: int, db: Session, id_supervisor: int = None) -> None:
    try:
        solicitud_historial = ApprovalRequestHistory(
            approval_request_id=id_solicitud,
            approval_role_id=id_rol_aprobacion,
            approval_status_id=ESTADO_APROBACION_PENDIENTE,
            created_at=datetime.now(),
            received_at=datetime.now(),
            comments=None,
            step_id=id_ruta,
            user_id=id_supervisor
        )
        asignar_usuario_aprobo_si_aplica(solicitud_historial, db)
        db.add(solicitud_historial)
        db.commit()
    except Exception as e:
        logging.error(f"Error al asignar siguiente paso: {e}")
        db.rollback()



def obtener_usuarios_disponibles_ajuste(solicitud: ApprovalRequests, db: Session) -> list[dict]:
    if solicitud.current_step is None or solicitud.current_step <= 1:
        return []

    historial = ApprovalRequestHistoryRepository.obtener_usuarios_disponibles_ajuste(solicitud.approval_request_id, solicitud.current_step, db)

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
    solicitud = ApprovalRequestsRepository.obtener_solicitud_por_registro_categoria(id_registro_asociado, db)
    respuesta = ResponseRequest(solicitud_exitosa=True)
    if not solicitud:
        return ResponseRequest(solicitud_exitosa=False, mensaje="{}")

    usuario_actual = UsuariosRepository.obtener_por_guid_msft(user_oid, db)

    solicitudHistorial = ApprovalRequestHistoryRepository.obtener_historial_ultima_aprobacion(id_registro_asociado, id_categoria, db)
    if not solicitudHistorial:
        content={
            "usuario_solicito": True if str(guid_solicitante) == str(user_oid) else False,
            "mensaje": "No se encontró una solicitud de aprobación para el ID y categoría proporcionados."
        }
        respuesta = ResponseRequest(solicitud_exitosa=False, mensaje=json.dumps(content))
        return respuesta

    flujoRuta = FlujosAprobacionService.obtener_flujo_aprobacion_ruta_orden(
        id_categoria, usuario_actual.id, solicitudHistorial.step_order, solicitudHistorial.approval_workflow_id, db
    )

    # paso_actual = _obtener_paso_actual(solicitud, db)
    # historial_pendiente = _obtener_historial_pendiente(solicitud, paso_actual, db)
    # usuarios_disponibles_ajustes = obtener_usuarios_disponibles_ajuste(solicitud, db)
    # puede_actuar = _usuario_puede_actuar(usuario_actual, paso_actual, historial_pendiente, db)

    # acciones = {
    #     "id_solicitud_aprobacion": solicitud.approval_request_id,
    #     "asigna_presupuesto_viajes": paso_actual.assign_travel_budget if paso_actual else False,
    #     "ajusta_itinerario_viajes": paso_actual.adjust_travel_itinerary if paso_actual else False,
    #     "valida_soportes": paso_actual.validate_supporting_documents if paso_actual else False,
    #     "valida_soportes_hotel": paso_actual.validate_hotel_documents if paso_actual else False,
    #     "deshabilita_conceptos_anticipo": paso_actual.disable_advance_concepts if paso_actual else False,
    #     "agrega_rpc": paso_actual.add_rpc if paso_actual else False,
    #     "agrega_documento_contable": paso_actual.add_accounting_document if paso_actual else False,
    #     "agrega_tarjeta_asistencia_medica": paso_actual.add_medical_assistance_card if paso_actual else False,
    #     "agrega_comprobante_egreso": paso_actual.add_expense_voucher if paso_actual else False,
    #     "habilitar_pago": paso_actual.enable_payment if paso_actual else False,
    #     "orden_actual": solicitud.current_step,
    #     "id_estado_aprobacion_ruta": historial_pendiente.approval_status_id if historial_pendiente else None,
    #     "usuarios_disponibles_ajustes": usuarios_disponibles_ajustes,
    #     "usuario_solicito": str(guid_solicitante) == str(user_oid) if guid_solicitante else False,
    #     "habilitar_solicitar_ajustes": len(usuarios_disponibles_ajustes) > 0,
    #     "id_estado_solicitud": solicitud.approval_status_id,
    # }

    # return ResponseRequest(
    #     solicitud_exitosa=puede_actuar,
    #     mensaje=json.dumps(acciones),
    #     identity=solicitud.approval_request_id,
    # )

    if not flujoRuta or (flujoRuta.is_supervisor and ((solicitudHistorial.user_id != usuario_actual.id))):
        print("No se encontró un flujo de aprobación válido o el usuario no tiene permisos.")
        respuesta.solicitud_exitosa = False
        content={
            "mensaje": "No se encontró un flujo de aprobación pendiente para la solicitud y usuario proporcionados."
        }
        respuesta.mensaje = json.dumps(content)
        return respuesta
    else:
        if solicitudHistorial.approval_status_id == ESTADO_APROBACION_PENDIENTE or (solicitudHistorial.approval_status_id == ESTADO_APROBACION_AJUSTES and usuario_actual.id == solicitudHistorial.user_id):
            usuarios_disponibles_ajustes = []
            # if solicitudHistorial.orden > 2:
            validaciones = validar_aprobaciones_anteriores(solicitudHistorial.approval_request_id, solicitudHistorial.step_order, db)
            if len(validaciones) > 0:
                usuario_disponible = {}
                for aprobacion in validaciones:
                    if not any(u["id_rol_aprobacion_ajuste"] == aprobacion.approval_role_id for u in usuarios_disponibles_ajustes):
                        usuario_disponible = {
                            "id_rol_aprobacion_ajuste": aprobacion.approval_role_id,
                            "usuario": f'{aprobacion.rol} ({aprobacion.user})',
                            "id_usuario_ajuste": aprobacion.user_id
                        }
                        usuarios_disponibles_ajustes.append(usuario_disponible)


            content={
                "usuario_solicito": True if flujoRuta.step_order == 1 and str(user_oid).strip() == str(guid_solicitante).strip() else False,
                "orden_actual": solicitudHistorial.step_order,
                "id_estado_aprobacion_ruta": solicitudHistorial.approval_status_step_id,
                "usuarios_disponibles_ajustes": usuarios_disponibles_ajustes,
                "habilitar_solicitar_ajustes": False if solicitudHistorial.approval_status_id == ESTADO_APROBACION_AJUSTES and usuario_actual.id == solicitudHistorial.user_id else True,
                "id_estado_solicitud": solicitudHistorial.approval_status_id
            }
            respuesta = ResponseRequest(solicitud_exitosa=True, mensaje=json.dumps(content))
        elif solicitudHistorial.approval_status_id == ESTADO_APROBACION_AJUSTES and flujoRuta.step_order == 1 and str(user_oid).strip() == str(guid_solicitante).strip():
            respuesta.solicitud_exitosa = True
            content={
                "usuario_solicito": True if flujoRuta.step_order == 1 and str(user_oid).strip() == str(guid_solicitante).strip() else False,
                "orden_actual": flujoRuta.step_order
            }
            respuesta.mensaje = json.dumps(content)
        else:
            respuesta.solicitud_exitosa = False
            content={
                "mensaje": "La solicitud de aprobación ya ha sido procesada para el paso correspondiente.",
                "usuario_solicito": False
            }
            respuesta.mensaje = json.dumps(content)

    return respuesta

def validar_aprobaciones_anteriores(id_solicitud_aprobacion: int, orden: int, db: Session) -> list[VWApprovalRequestHistory]:
    try:
        aprobaciones_anteriores = ApprovalRequestHistoryRepository.obtener_historial_aprovaciones_previas_pendientes(id_solicitud_aprobacion, orden, [ESTADO_APROBACION_PENDIENTE, ESTADO_APROBACION_AJUSTES], db)

        return aprobaciones_anteriores
    except Exception as e:
        logging.error(f"Error al validar aprobaciones anteriores: {e}")
        raise


def marcar_historial_resuelto(historial: ApprovalRequestHistory, estado_aprobacion: int, usuario_actual: Users, comentarios: str | None, db: Session) -> None:
    historial.approval_status_id = estado_aprobacion
    historial.comments = comentarios if comentarios is not None else historial.comments
    historial.approved_at = datetime.now()
    historial.approver_user_id = usuario_actual.id
    historial.approved_by_user = obtener_usuario_aprobo(usuario_actual.id, db)
    historial.user_id = usuario_actual.id


def resolver_destino_ajuste(solicitud: ApprovalRequests, accion: AccionSolicitudAprobacion, db: Session) -> tuple[ApprovalFlowStep | None, int | None, int | None]:
    usuarios_disponibles = obtener_usuarios_disponibles_ajuste(solicitud, db)
    id_rol = accion.id_rol_aprobacion_ajuste or (usuarios_disponibles[0]["id_rol_aprobacion_ajuste"] if usuarios_disponibles else None)
    id_usuario = accion.id_usuario_ajuste if accion.id_usuario_ajuste is not None else (usuarios_disponibles[0]["id_usuario_ajuste"] if usuarios_disponibles else None)
    if id_rol is None:
        return None, None, None

    paso = ApprovalFlowRepository.obtener_paso_requiere_ajuste(solicitud.approval_workflow_id, id_rol, solicitud.current_step, db)
    return paso, id_rol, id_usuario


def actualizar_ruta(accion: AccionSolicitudAprobacion, id_categoria: int, id_usuario: int, db: Session, id_supervisor: int = None, identity: int = None) -> ResponseRequest:
    respuesta = ResponseRequest(solicitud_exitosa=True)
    id_flujo_aprobacion = 0
    try:
        solicitudHistorial = ApprovalRequestHistoryRepository.obtener_historial_ultima_accion(accion.id_solicitud_aprobacion, identity, id_categoria, db)
        # orden = solicitudHistorial.orden if accion.tipo_accion != "SOLICITUD_AJUSTADA" else 1
        orden = accion.orden_actual
        flujoRuta = FlujosAprobacionService.obtener_flujo_aprobacion_ruta_orden(
            id_categoria, id_usuario, orden, solicitudHistorial.approval_workflow_id, db
        )
        id_flujo_aprobacion = solicitudHistorial.approval_workflow_id
        if not flujoRuta:
            respuesta.solicitud_exitosa = False
            respuesta.mensaje = "No se encontró un flujo de aprobación pendiente para la solicitud y usuario proporcionados."
            print("No se encontró un flujo de aprobación pendiente para la solicitud y usuario proporcionados.")
        else:
            solicitudRuta = ApprovalRequestHistoryRepository.obtener_ruta(accion.id_solicitud_aprobacion, ESTADO_APROBACION_PENDIENTE, db)

            if solicitudRuta.step_id != flujoRuta.step_id:
                respuesta.solicitud_exitosa = False
                respuesta.mensaje = "El paso actual del flujo de aprobación no corresponde al usuario que esta realizando la acción."
            else:

                solicitudRuta.approval_status_id = ESTADO_APROBACION_APROBADO if accion.tipo_accion == "APROBAR" else ESTADO_APROBACION_AJUSTES_REALIZADOS if accion.tipo_accion == "SOLICITUD_AJUSTADA" else ESTADO_APROBACION_AJUSTES
                
                solicitudRuta.approved_at = datetime.now()
                solicitudRuta.comments = accion.comentarios
                solicitudRuta.user_id = id_usuario if solicitudRuta.user_id is None else solicitudRuta.user_id
                # solicitudRuta.id_usuarios_mencion = accion.id_usuarios_mencion
                solicitudRuta.user_id = id_usuario
                asignar_usuario_aprobo_si_aplica(solicitudRuta, db)
                db.commit()
                db.refresh(solicitudRuta)
                solicitud = ApprovalRequestsRepository.obtener_solicitud(accion.id_solicitud_aprobacion, db)
                if accion.tipo_accion == "APROBAR":
                    # Obtener siguiente paso en la ruta
                    flujoPasosAprobacion = FlujosAprobacionService.obtener_flujo_aprobacion_pasos(id_flujo_aprobacion, db)
                    if flujoPasosAprobacion == solicitudHistorial.step_order:
                        # Actualizar estado final de la solicitud de aprobación
                        solicitud.approval_status_id = ESTADO_APROBACION_FINALIZADO
                        solicitudRuta.approval_status_id = ESTADO_APROBACION_FINALIZADO
                        db.commit()
                        db.refresh(solicitud)
                        respuesta.mensaje = "RUTA_COMPLETA"
                    else:
                        # Asignar siguiente paso
                        solicitudHistorial = ApprovalRequestHistoryRepository.obtener_historial_ultima_aprobacion(identity, id_categoria, db)

                        id_rol_aprobacion, id_ruta, es_supervisor = FlujosAprobacionService.obtener_siguiente_paso_ruta(
                            solicitudHistorial.category_id, solicitudHistorial.step_order, id_flujo_aprobacion,  db
                        )
                        if es_supervisor == False:
                            id_supervisor = None
                        solicitud.current_step = solicitud.current_step + 1
                        solicitud.approval_status_id = ESTADO_APROBACION_PENDIENTE
                        db.commit()
                        db.refresh(solicitud)
                        asignar_siguiente_paso(
                            accion.id_solicitud_aprobacion,
                            id_rol_aprobacion,
                            id_ruta,
                            db,
                            id_supervisor
                        )
                        respuesta.mensaje = "EN_PROCESO"
                elif accion.tipo_accion == "AJUSTAR":
                    # Asignar siguiente paso
                    solicitudHistorial = ApprovalRequestHistoryRepository.obtener_historial_ultima_aprobacion(identity, id_categoria, db)
                    
                    paso_actual = 1
                    id_usuario_aprobacion = None
                    if accion.id_usuario_ajuste is not None:
                        id_rol_aprobacion, id_ruta, es_supervisor, orden = FlujosAprobacionService.obtener_rol_solicitud_ajuste(
                            solicitudHistorial.category_id, id_flujo_aprobacion, accion.id_rol_aprobacion_ajuste, accion.id_usuario_ajuste, db
                        )
                        paso_actual = orden
                        id_usuario_aprobacion = accion.id_usuario_ajuste
                    else:
                        id_rol_aprobacion, id_ruta, es_supervisor = FlujosAprobacionService.obtener_siguiente_paso_ruta(
                            solicitudHistorial.category_id, 0, id_flujo_aprobacion,  db
                        )
                        # if es_supervisor == False:
                        #     id_supervisor = None
                    solicitud.current_step = paso_actual
                    solicitud.approval_status_id = ESTADO_APROBACION_AJUSTES
                    db.commit()
                    db.refresh(solicitud)
                    asignar_siguiente_paso(
                        accion.id_solicitud_aprobacion,
                        id_rol_aprobacion,
                        id_ruta,
                        db,
                        id_usuario_aprobacion
                    )
                    respuesta.mensaje = "AJUSTES"
                elif accion.tipo_accion == "SOLICITUD_AJUSTADA":
                    
                    solicitudHistorial = ApprovalRequestHistoryRepository.obtener_historial_ultimas_dos_aprobaciones(identity, id_categoria, db)

                    # db.query(VWApprovalRequestHistory).filter(
                    #     VWApprovalRequestHistory.related_record_id == identity,
                    #     VWApprovalRequestHistory.category_id == id_categoria
                    # ).order_by(VWApprovalRequestHistory.step_order.desc()).limit(2).all()
                    

                    # id_rol_aprobacion, id_ruta = FlujosAprobacionService.obtener_siguiente_paso_ruta(
                    #     solicitudHistorial.id_categoria, 0, id_flujo_aprobacion,  db
                    # )
                    solicitud.approval_status_id = ESTADO_APROBACION_PENDIENTE
                    solicitudHistorial = sorted(solicitudHistorial, key=lambda x: x.step_order)
                    siguientePaso = solicitudHistorial[1]
                    if siguientePaso.is_supervisor == False:
                        id_supervisor = None
                    solicitud.current_step = siguientePaso.step_order
                    db.commit()
                    db.refresh(solicitud)
                    asignar_siguiente_paso(
                        accion.id_solicitud_aprobacion,
                        siguientePaso.approval_role_id,
                        siguientePaso.step_id,
                        db,
                        id_supervisor
                    )
                    respuesta.mensaje = "EN_PROCESO"
                respuesta.solicitud_exitosa = True
        return respuesta
    except Exception as e:
        logging.error(f"Error al actualizar ruta: {e}")
        raise
