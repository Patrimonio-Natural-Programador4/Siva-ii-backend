from fastapi import BackgroundTasks
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from dto.ListaGenerica import ListaGenerica
from dto.ListadosDTO import Listados
from dto.ResponseRequest import ResponseRequest
from dto.ViajesDTO import ViajesCreate, ViajesListSP
from dto.AccionesSolicitudAprobacionDTO import AccionSolicitudAprobacion
from dto.ViajesHotelDTO import ViajesHotelBase
from dto.ViajesItinerarioDTO import ViajesItinerarioBase
from entity.travel_accommodations import TravelAccommodations
from entity.travel_itineraries import TravelItineraries
from entity.travel_requests import TravelRequests
from entity.travel_status import TravelStatus
from entity.banks import Banks
from entity.account_types import AccountTypes
from repository import ConceptoAnticiposRepository, EntidadBancariaRepository, RegionsRepository, RoleApprovalSupervisorUsersRepository, RubrosRepository, TipoCuentaRepository, UsersProgramsRepository, UsersProgramsRepository, UsuariosRepository, ViajesHotelRepository, ViajesItinerarioRepository, ViajesRepository, ProgramsRepository
from exceptions import PruebaCreationError, PruebaNotFoundError
import logging
from datetime import date, datetime, time
from jinja2 import Environment, FileSystemLoader
from services import SolicitudesAprobacionService, NotificacionesService
from entity.users import Users

CATEGORIA_APROBACION_SOLICITUD_VIAJE = "SOL_VIA_ANT"

def crear_viaje(viaje: ViajesCreate, db: Session, usuario_guid: str, background_tasks: BackgroundTasks) -> ResponseRequest:
    respuesta = ResponseRequest(solicitud_exitosa=True)
    try:
       
        usuario = UsuariosRepository.obtener_por_guid_msft(usuario_guid.strip(), db)
        anio_actual = date.today().year
        # usuario.habilitar_solicitud_viaje = False
        fecha_actual = date.today()
        viajes = ViajesRepository.numero_viajes(db)
        nuevo_viaje = TravelRequests()

        nuevo_viaje.code = f"V-{fecha_actual.year}-{viajes + 1:02d}"
        nuevo_viaje.created_at = datetime.now()
        nuevo_viaje.created_by_user_id = usuario.id
        nuevo_viaje.traveler_user_id = usuario.id
        nuevo_viaje.travel_start_date = viaje.fecha_inicio_viaje
        nuevo_viaje.travel_end_date = viaje.fecha_fin_viaje
        nuevo_viaje.activity_purpose = viaje.objetivo
        nuevo_viaje.account_number = viaje.numero_cuenta
        nuevo_viaje.account_type_id = viaje.id_tipo_cuenta
        nuevo_viaje.bank_id = viaje.id_entidad_bancaria
        nuevo_viaje.requires_tickets = viaje.requiere_tiquetes
        nuevo_viaje.requires_advance_payment = viaje.requiere_anticipo
        nuevo_viaje.travel_status_id = 1
        nuevo_viaje.is_international = viaje.viaje_internacional
        nuevo_viaje.country = viaje.pais
        nuevo_viaje.is_guest = viaje.es_invitado
        nuevo_viaje.guest_name = viaje.persona_invitada
        nuevo_viaje.guest_document = viaje.documento_persona_invitada if viaje.es_invitado else usuario.identification_number
        nuevo_viaje.guest_phone = viaje.telefono_persona_invitada
        nuevo_viaje.guest_email = viaje.correo_persona_invitada if viaje.es_invitado else usuario.email
        nuevo_viaje.supervisor_approval_role_id = viaje.id_rol_aprobacion_supervisor
        nuevo_viaje.supervisor_user_id = viaje.id_supervisor_aprueba
        nuevo_viaje.additional_comments = viaje.observaciones_adicionales
        nuevo_viaje.mentions_json = viaje.menciones_json
        nuevo_viaje.mentioned_user_ids = viaje.id_usuarios_mencion
        nuevo_viaje.program_id = viaje.id_programa
        nuevo_viaje.advance_amount = viaje.valor_anticipo
        nuevo_viaje.rubro_id = viaje.id_rubro
        nuevo_viaje.activity_id = viaje.id_actividad
        nuevo_viaje.year_rubro = anio_actual
        nuevo_viaje.short_rubro = viaje.rubro_corto
        nuevo_viaje.emergency_contact = viaje.contacto_emergencia
        nuevo_viaje.emergency_phone = viaje.telefono_emergencia
        nuevo_viaje.emergency_relationship = viaje.parentesco_emergencia
        nuevo_viaje.traveler_birth_date = viaje.fecha_nacimiento_viajero

        # if(viaje.es_invitado):
        #     nuevo_viaje.traveler_birth_date = viaje.fecha_nacimiento_viajero
        # else:
        #     nuevo_viaje.traveler_birth_date = usuario.fecha_nacimiento
        #     nuevo_viaje.guest_phone = usuario.telefono
        nuevo_viaje.start_time = viaje.hora_inicio
        nuevo_viaje.end_time = viaje.hora_fin

        # if viaje.guid_soporte_pasaporte.strip() != "":
        #     tmpFile = db.query(TmpSoportes).filter(TmpSoportes.guid == viaje.guid_soporte_pasaporte).first()
        #     if not tmpFile:
        #         raise PruebaNotFoundError("Soporte pasaporte no encontrado")
        #     else:
        #         nuevo_viaje.soporte_pasaporte = tmpFile.soporte
        #         nuevo_viaje.ruta_soporte_pasaporte = tmpFile.ruta_soporte
        db.add(nuevo_viaje)
        db.commit()
        db.refresh(nuevo_viaje)

        tiene_anticipo = False

        if viaje.hotel:
            actualizar_hotel_viaje(nuevo_viaje.travel_request_id, viaje.hotel, db)
        if viaje.itinerario:
            actualizar_itinerario_viaje(nuevo_viaje.travel_request_id, viaje.itinerario, db)
        # if viaje.anticipo.detalle:
        #     tiene_anticipo = True
        #     viaje.anticipo.id_tipo_cuenta = viaje.id_tipo_cuenta
        #     viaje.anticipo.nombre_tercero = f"{usuario.first_name} {usuario.other_name} {usuario.last_name} {usuario.other_last_name}"
        #     # AnticiposService.actualizar_anticipo(1, nuevo_viaje.travel_request_id, viaje.anticipo, db, usuario.id_usuario)
        #     # actualizar_anticipo(nuevo_viaje.id_viaje, viaje.anticipo, db)


        if viaje.enviar_aprobacion:
            id_categoria_aprobacion = SolicitudesAprobacionService.obtener_categoria_aprobacion(CATEGORIA_APROBACION_SOLICITUD_VIAJE, db)
            if not id_categoria_aprobacion:
                raise PruebaCreationError(f"No se encontró la categoría de aprobación con el código {CATEGORIA_APROBACION_SOLICITUD_VIAJE}")
            id_solicitud_aprobacion = SolicitudesAprobacionService.crear_solicitud_aprobacion(id_categoria_aprobacion, nuevo_viaje.travel_request_id, usuario.id, nuevo_viaje.code, db, nuevo_viaje.supervisor_user_id, nuevo_viaje.program_id)
            nuevo_viaje.approval_request_id = id_solicitud_aprobacion
            nuevo_viaje.travel_status_id = 2
            nuevo_viaje.current_request_order = 2
            db.commit()

            

            viaje.codigo = nuevo_viaje.code
            db.refresh(nuevo_viaje)
            historialAprobacionSolicitud = SolicitudesAprobacionService.obtener_solicitud_aprobacion_por_id_asociado_id_categoria(nuevo_viaje.travel_request_id, id_categoria_aprobacion, db)

            itinerario = ViajesItinerarioRepository.listar_itinerarios_por_viaje(nuevo_viaje.travel_request_id, db)
            hoteles = ViajesHotelRepository.listar_hoteles_por_viaje(nuevo_viaje.travel_request_id, db)
            # anticipos = AnticiposDetalleRepository.listar_anticipos_por_viaje(viajeDb.id_viaje, db)
            # anticipo = AnticiposReintegrosRepository.obtener_anticipo_reintegro_por_tipo_y_relacion(1, nuevo_viaje.travel_request_id, False, db)
            # reintegro = AnticiposReintegrosRepository.obtener_anticipo_reintegro_por_tipo_y_relacion(1, nuevo_viaje.travel_request_id, True, db)
            # viajeDTO = viajeCreateDTO(nuevo_viaje, itinerario, hoteles, anticipo, reintegro, db)
            # Resolviendo nombre y apellidos del solicitante
            nombre_usuario = ' '.join(
                part.strip()
                for part in [usuario.first_name, usuario.other_name or '', usuario.last_name, usuario.other_last_name or '']
                if part and part.strip()
            )
            
            # Resolviendo nombre del banco
            entidad_bancaria = ""
            if nuevo_viaje.bank_id:
                bank_row = db.query(Banks).filter(Banks.bank_id == nuevo_viaje.bank_id).first()
                if bank_row:
                    entidad_bancaria = bank_row.bank
            
            # Resolviendo tipo de cuenta
            tipo_cuenta = ""
            if nuevo_viaje.account_type_id:
                acc_type_row = db.query(AccountTypes).filter(AccountTypes.account_type_id == nuevo_viaje.account_type_id).first()
                if acc_type_row:
                    tipo_cuenta = acc_type_row.account_type

            # Calcular número de días e itinerario horas
            nro_dias = 0
            nro_horas = 0
            if nuevo_viaje.travel_start_date and nuevo_viaje.travel_end_date:
                delta = nuevo_viaje.travel_end_date - nuevo_viaje.travel_start_date
                nro_dias = delta.days
                nro_horas = nro_dias * 24

            template_data = {
                "codigo": nuevo_viaje.code,
                "usuario": nombre_usuario,
                "identificacion": usuario.identification_number if usuario.identification_number else "",
                "fecha_solicitud": nuevo_viaje.created_at.strftime("%Y-%m-%d") if nuevo_viaje.created_at else date.today().strftime("%Y-%m-%d"),
                "categoria": "Solicitud de viaje y anticipo",
                "fecha_inicio_viaje": nuevo_viaje.travel_start_date,
                "fecha_fin_viaje": nuevo_viaje.travel_end_date,
                "hora_inicio": nuevo_viaje.start_time.strftime("%H:%M") if nuevo_viaje.start_time else "",
                "hora_fin": nuevo_viaje.end_time.strftime("%H:%M") if nuevo_viaje.end_time else "",
                "nro_dias": nro_dias,
                "nro_horas": nro_horas,
                "es_invitado": nuevo_viaje.is_guest,
                "persona_invitada": nuevo_viaje.guest_name,
                "documento_persona_invitada": nuevo_viaje.guest_document,
                "telefono_persona_invitada": nuevo_viaje.guest_phone,
                "correo_persona_invitada": nuevo_viaje.guest_email,
                "fecha_nacimiento_viajero": nuevo_viaje.traveler_birth_date,
                "viaje_internacional": nuevo_viaje.is_international,
                "pais": nuevo_viaje.country,
                "asociado_taller": False,
                "requiere_anticipo": nuevo_viaje.requires_advance_payment,
                "tipo_cuenta": tipo_cuenta,
                "entidad_bancaria": entidad_bancaria,
                "numero_cuenta": nuevo_viaje.account_number,
                "objetivo_actividad": nuevo_viaje.activity_purpose,
                "observaciones_adicionales": nuevo_viaje.additional_comments,
                "itinerario": viaje.itinerario,
                "hotel": viaje.hotel,
                "anticipo": viaje.anticipo,
                "historialAprobacionSolicitud": historialAprobacionSolicitud
            }

            env = Environment(loader=FileSystemLoader(''))
            template = env.get_template('templates/notificacion_sv.html')
            html_out = template.render(**template_data)

            # Obtener destinatarios de correo
            destinatarios = []
            if nuevo_viaje.supervisor_user_id:
                supervisor = db.query(Users).filter(Users.id == nuevo_viaje.supervisor_user_id).first()
                if supervisor and supervisor.email:
                    destinatarios.append(supervisor.email)
            
            if usuario and usuario.email and usuario.email not in destinatarios:
                destinatarios.append(usuario.email)

            if nuevo_viaje.mentioned_user_ids:
                for m_id in nuevo_viaje.mentioned_user_ids:
                    m_user = db.query(Users).filter(Users.id == m_id).first()
                    if m_user and m_user.email and m_user.email not in destinatarios:
                        destinatarios.append(m_user.email)

            to_recipients = [{"emailAddress": {"address": correo}} for correo in destinatarios]
            
            if to_recipients:
                background_tasks.add_task(
                    NotificacionesService.solicitud_viaje,
                    f"Solicitud de viaje {nuevo_viaje.code} enviada por aprobación",
                    to_recipients,
                    html_out,
                    "",
                    "",
                    db
                )


        respuesta.identity = nuevo_viaje.travel_request_id
        respuesta.mensaje = "Viaje creado exitosamente"
        return respuesta
    except Exception as e:
        logging.error(f"Failed to create viaje: {str(e)}")
        return ResponseRequest(
            solicitud_exitosa=False,
            mensaje=str(e)
        )
        # raise PruebaCreationError(str(e))

def actualizar_viaje(guid: str, viaje: ViajesCreate, db: Session, usuario_guid: str, background_tasks: BackgroundTasks) -> ResponseRequest:
    respuesta = ResponseRequest(solicitud_exitosa=True)
    try:
       
        usuario = UsuariosRepository.obtener_por_guid_msft(usuario_guid.strip(), db)
        viajeDb = ViajesRepository.obtener_por_guid(guid.strip(), db)
        if not viajeDb:
            raise PruebaNotFoundError("Viaje no encontrado")

        
        viajeDb.updated_at = datetime.now()
        viajeDb.updated_by_user_id = usuario.id
        viajeDb.traveler_user_id = usuario.id
        viajeDb.travel_start_date = viaje.fecha_inicio_viaje
        viajeDb.travel_end_date = viaje.fecha_fin_viaje
        viajeDb.activity_purpose = viaje.objetivo
        viajeDb.account_number = viaje.numero_cuenta
        viajeDb.account_type_id = viaje.id_tipo_cuenta
        viajeDb.bank_id = viaje.id_entidad_bancaria
        viajeDb.requires_tickets = viaje.requiere_tiquetes
        viajeDb.requires_advance_payment = viaje.requiere_anticipo
        viajeDb.is_international = viaje.viaje_internacional
        viajeDb.country = viaje.pais
        viajeDb.is_guest = viaje.es_invitado
        viajeDb.guest_name = viaje.persona_invitada
        viajeDb.guest_document = viaje.documento_persona_invitada
        viajeDb.guest_phone = viaje.telefono_persona_invitada
        viajeDb.guest_email = viaje.correo_persona_invitada
        viajeDb.supervisor_approval_role_id = viaje.id_rol_aprobacion_supervisor
        viajeDb.supervisor_user_id = viaje.id_supervisor_aprueba
        viajeDb.additional_comments = viaje.observaciones_adicionales
        viajeDb.mentions_json = viaje.menciones_json
        viajeDb.mentioned_user_ids = viaje.id_usuarios_mencion
        viajeDb.program_id = viaje.id_programa
        viajeDb.advance_amount = viaje.valor_anticipo
        viajeDb.rubro_id = viaje.id_rubro
        viajeDb.activity_id = viaje.id_actividad
        viajeDb.short_rubro = viaje.rubro_corto
        viajeDb.emergency_contact = viaje.contacto_emergencia
        viajeDb.emergency_phone = viaje.telefono_emergencia
        viajeDb.emergency_relationship = viaje.parentesco_emergencia
        viajeDb.traveler_birth_date = viaje.fecha_nacimiento_viajero
        # if(viaje.es_invitado):
        #     viajeDb.traveler_birth_date = viaje.fecha_nacimiento_viajero
        # else:
        #     viajeDb.traveler_birth_date = usuario.fecha_nacimiento
        #     viajeDb.guest_phone = usuario.telefono
        viajeDb.start_time = viaje.hora_inicio
        viajeDb.end_time = viaje.hora_fin

        # if viaje.guid_soporte_pasaporte.strip() != "":
        #     tmpFile = db.query(TmpSoportes).filter(TmpSoportes.guid == viaje.guid_soporte_pasaporte).first()
        #     if not tmpFile:
        #         raise PruebaNotFoundError("Soporte pasaporte no encontrado")
        #     else:
        #         viajeDb.soporte_pasaporte = tmpFile.soporte
        #         viajeDb.ruta_soporte_pasaporte = tmpFile.ruta_soporte
        db.commit()
        db.refresh(viajeDb)

        tiene_anticipo = False

        if viaje.hotel:
            actualizar_hotel_viaje(viajeDb.travel_request_id, viaje.hotel, db)
        if viaje.itinerario:
            actualizar_itinerario_viaje(viajeDb.travel_request_id, viaje.itinerario, db)
        # if viaje.anticipo.detalle:
        #     tiene_anticipo = True
        #     viaje.anticipo.id_tipo_cuenta = viaje.id_tipo_cuenta
        #     viaje.anticipo.nombre_tercero = f"{usuario.first_name} {usuario.other_name} {usuario.last_name} {usuario.other_last_name}"
        #     # AnticiposService.actualizar_anticipo(1, viajeDb.travel_request_id, viaje.anticipo, db, usuario.id_usuario)
        #     # actualizar_anticipo(viajeDb.id_viaje, viaje.anticipo, db)


        if viaje.enviar_aprobacion:
            id_categoria_aprobacion = SolicitudesAprobacionService.obtener_categoria_aprobacion(CATEGORIA_APROBACION_SOLICITUD_VIAJE, db)
            if not id_categoria_aprobacion:
                raise PruebaCreationError(f"No se encontró la categoría de aprobación con el código {CATEGORIA_APROBACION_SOLICITUD_VIAJE}")
            id_solicitud_aprobacion = SolicitudesAprobacionService.crear_solicitud_aprobacion(id_categoria_aprobacion, viajeDb.travel_request_id, usuario.id, viajeDb.code, db, viajeDb.supervisor_user_id, viajeDb.program_id)
            viajeDb.approval_request_id = id_solicitud_aprobacion
            viajeDb.travel_status_id = 2
            viajeDb.current_request_order = 2
            db.commit()
            db.refresh(viajeDb)
            historialAprobacionSolicitud = SolicitudesAprobacionService.obtener_solicitud_aprobacion_por_id_asociado_id_categoria(viajeDb.travel_request_id, id_categoria_aprobacion, db)

            itinerario = ViajesItinerarioRepository.listar_itinerarios_por_viaje(viajeDb.travel_request_id, db)
            hoteles = ViajesHotelRepository.listar_hoteles_por_viaje(viajeDb.travel_request_id, db)
            # anticipos = AnticiposDetalleRepository.listar_anticipos_por_viaje(viajeDb.id_viaje, db)
            # anticipo = AnticiposReintegrosRepository.obtener_anticipo_reintegro_por_tipo_y_relacion(1, nuevo_viaje.travel_request_id, False, db)
            # reintegro = AnticiposReintegrosRepository.obtener_anticipo_reintegro_por_tipo_y_relacion(1, nuevo_viaje.travel_request_id, True, db)
            # viajeDTO = viajeCreateDTO(nuevo_viaje, itinerario, hoteles, anticipo, reintegro, db)
            # Resolviendo nombre y apellidos del solicitante
            nombre_usuario = ' '.join(
                part.strip()
                for part in [usuario.first_name, usuario.other_name or '', usuario.last_name, usuario.other_last_name or '']
                if part and part.strip()
            )
            
            # Resolviendo nombre del banco
            entidad_bancaria = ""
            if viajeDb.bank_id:
                bank_row = db.query(Banks).filter(Banks.bank_id == viajeDb.bank_id).first()
                if bank_row:
                    entidad_bancaria = bank_row.bank
            
            # Resolviendo tipo de cuenta
            tipo_cuenta = ""
            if viajeDb.account_type_id:
                acc_type_row = db.query(AccountTypes).filter(AccountTypes.account_type_id == viajeDb.account_type_id).first()
                if acc_type_row:
                    tipo_cuenta = acc_type_row.account_type

            # Calcular número de días e itinerario horas
            nro_dias = 0
            nro_horas = 0
            if viajeDb.travel_start_date and viajeDb.travel_end_date:
                delta = viajeDb.travel_end_date - viajeDb.travel_start_date
                nro_dias = delta.days
                nro_horas = nro_dias * 24

            template_data = {
                "codigo": viajeDb.code,
                "usuario": nombre_usuario,
                "identificacion": usuario.identification_number if usuario.identification_number else "",
                "fecha_solicitud": viajeDb.created_at.strftime("%Y-%m-%d") if viajeDb.created_at else date.today().strftime("%Y-%m-%d"),
                "categoria": "Solicitud de viaje y anticipo",
                "fecha_inicio_viaje": viajeDb.travel_start_date,
                "fecha_fin_viaje": viajeDb.travel_end_date,
                "hora_inicio": viajeDb.start_time.strftime("%H:%M") if viajeDb.start_time else "",
                "hora_fin": viajeDb.end_time.strftime("%H:%M") if viajeDb.end_time else "",
                "nro_dias": nro_dias,
                "nro_horas": nro_horas,
                "es_invitado": viajeDb.is_guest,
                "persona_invitada": viajeDb.guest_name,
                "documento_persona_invitada": viajeDb.guest_document,
                "telefono_persona_invitada": viajeDb.guest_phone,
                "correo_persona_invitada": viajeDb.guest_email,
                "fecha_nacimiento_viajero": viajeDb.traveler_birth_date,
                "viaje_internacional": viajeDb.is_international,
                "pais": viajeDb.country,
                "asociado_taller": False,
                "requiere_anticipo": viajeDb.requires_advance_payment,
                "tipo_cuenta": tipo_cuenta,
                "entidad_bancaria": entidad_bancaria,
                "numero_cuenta": viajeDb.account_number,
                "objetivo_actividad": viajeDb.activity_purpose,
                "observaciones_adicionales": viajeDb.additional_comments,
                "itinerario": viaje.itinerario,
                "hotel": viaje.hotel,
                "historialAprobacionSolicitud": historialAprobacionSolicitud
            }

            env = Environment(loader=FileSystemLoader(''))
            template = env.get_template('templates/notificacion_sv.html')
            html_out = template.render(**template_data)

            # Obtener destinatarios de correo
            destinatarios = []
            if viajeDb.supervisor_user_id:
                supervisor = db.query(Users).filter(Users.id == viajeDb.supervisor_user_id).first()
                if supervisor and supervisor.email:
                    destinatarios.append(supervisor.email)
            
            if usuario and usuario.email and usuario.email not in destinatarios:
                destinatarios.append(usuario.email)

            if viajeDb.mentioned_user_ids:
                for m_id in viajeDb.mentioned_user_ids:
                    m_user = db.query(Users).filter(Users.id == m_id).first()
                    if m_user and m_user.email and m_user.email not in destinatarios:
                        destinatarios.append(m_user.email)

            to_recipients = [{"emailAddress": {"address": correo}} for correo in destinatarios]
            
            if to_recipients:
                background_tasks.add_task(
                    NotificacionesService.solicitud_viaje,
                    f"Solicitud de viaje {viajeDb.code} enviada por aprobación",
                    to_recipients,
                    html_out,
                    "",
                    "",
                    db
                )


        respuesta.identity = viajeDb.travel_request_id
        respuesta.mensaje = "Viaje actualizado exitosamente"
        return respuesta
    except Exception as e:
        logging.error(f"Failed to update viaje: {str(e)}")
        return ResponseRequest(
            solicitud_exitosa=False,
            mensaje=str(e)
        )
        # raise PruebaCreationError(str(e))



def actualizar_itinerario_viaje(viaje_id: int, itinerarioList: list[ViajesItinerarioBase], db: Session, validar_eliminacion: bool = True) -> None:
    try:
        # Add new itinerario
        for item in itinerarioList:
            # if item.requiere_tiquetes_aereos and (item.id_proyecto is None or item.id_rubro is None):
            #     raise PruebaCreationError("Debe seleccionar proyecto y rubro para los itinerarios que requieren tiquetes aereos")

            if item.id_viaje_itinerario is None:
                nuevo_itinerario = TravelItineraries(
                    travel_request_id=viaje_id,
                    travel_date=item.fecha,
                    destination_municipality_id=item.id_municipio_destino,
                    origin_municipality_id=item.id_municipio_origen,
                    departure_time=item.hora,
                    comments=item.observaciones,
                    is_rural_area=item.es_zona_rural,
                    rural_area_comments=item.observaciones_zona_rural,
                    requires_air_tickets=item.requiere_tiquetes_aereos,
                    project_id=item.id_proyecto if item.requiere_tiquetes_aereos else None,
                    budget_item_id=item.id_rubro if item.requiere_tiquetes_aereos else None
                )
                db.add(nuevo_itinerario)
                db.commit()
                item.id_viaje_itinerario = nuevo_itinerario.travel_itinerary_id
            elif item.editado:
                editar_itinerario = ViajesItinerarioRepository.obtener_itinerario_por_id(item.id_viaje_itinerario, viaje_id, db)
                if editar_itinerario:
                    editar_itinerario.travel_date = item.fecha
                    editar_itinerario.destination_municipality_id = item.id_municipio_destino
                    editar_itinerario.origin_municipality_id = item.id_municipio_origen
                    editar_itinerario.departure_time = item.hora
                    editar_itinerario.comments = item.observaciones
                    editar_itinerario.is_rural_area=item.es_zona_rural
                    editar_itinerario.rural_area_comments=item.observaciones_zona_rural
                    editar_itinerario.requires_air_tickets = item.requiere_tiquetes_aereos
                    editar_itinerario.project_id = item.id_proyecto if item.requiere_tiquetes_aereos else None
                    editar_itinerario.budget_item_id = item.id_rubro if item.requiere_tiquetes_aereos else None
                    db.commit()
                else:
                    logging.warning(f"Itinerario with id {item.id_viaje_itinerario} not found for viaje {viaje_id}")

        itinerario_viaje = ViajesItinerarioRepository.listar_itinerarios_por_viaje(viaje_id, db)
        itinerarios_ids = {m.travel_itinerary_id for m in itinerario_viaje}

        itinerarios_list_ids = {itinerario.id_viaje_itinerario for itinerario in itinerarioList}
        itinerario_a_eliminar = []
        if validar_eliminacion:
            itinerario_a_eliminar = itinerarios_ids - itinerarios_list_ids

        for id_viaje_itinerario in itinerario_a_eliminar:
            # Eliminar el itinerario de la base de datos
            filas_eliminadas = db.query(TravelItineraries).filter(
                TravelItineraries.travel_itinerary_id == id_viaje_itinerario
            ).delete()
            logging.info(
                f"El itinerario {id_viaje_itinerario} ha sido eliminado para el viaje {viaje_id}. "
                f"Filas afectadas: {filas_eliminadas}"
            )

        if itinerario_a_eliminar:
            db.commit()

    except Exception as e:
        logging.error(f"Failed to update itinerario for viaje {viaje_id}: {str(e)}")
        raise PruebaCreationError(str(e))
    

    
def actualizar_hotel_viaje(viaje_id: int, hotelList: list[ViajesHotelBase], db: Session, validar_eliminacion: bool = True) -> None:
    try:
        # Add new hotel
        for item in hotelList:
            # if item.pago_gestiona_fundacion and (item.id_proyecto is None or item.id_rubro is None):
            #     raise PruebaCreationError("Debe seleccionar proyecto y rubro para los hoteles gestionados por fundacion")

            if item.id_viaje_hotel is None:
                print(viaje_id, "item.id_viaje_hotel", item.id_viaje_hotel)
                try:
                    nuevo_hotel = TravelAccommodations(
                        travel_request_id=viaje_id,
                        check_in_date=item.fecha_llegada,
                        check_out_date=item.fecha_salida,
                        municipality_id=item.id_municipio,
                        comments=item.observaciones,
                        accommodation_type=item.tipo_alojamiento,
                        foundation_managed_payment=item.pago_gestiona_fundacion,
                        project_id=item.id_proyecto if item.pago_gestiona_fundacion else None,
                        budget_item_id=item.id_rubro if item.pago_gestiona_fundacion else None
                    )
                    db.add(nuevo_hotel)
                    db.commit()
                    db.refresh(nuevo_hotel)
                    item.id_viaje_hotel = nuevo_hotel.travel_accommodation_id
                except Exception as e:
                    print(f"Error al crear nuevo hotel: {str(e)}")
                    logging.error(f"Error al guardar {viaje_id}: {str(e)}")
                    db.rollback()


            elif item.editado:
                editar_hotel = ViajesHotelRepository.obtener_hotel_por_id(item.id_viaje_hotel, viaje_id, db)
                if editar_hotel:
                    editar_hotel.check_in_date = item.fecha_llegada
                    editar_hotel.check_out_date = item.fecha_salida
                    editar_hotel.municipality_id = item.id_municipio
                    editar_hotel.comments = item.observaciones
                    editar_hotel.accommodation_type=item.tipo_alojamiento
                    editar_hotel.foundation_managed_payment=item.pago_gestiona_fundacion
                    editar_hotel.project_id = item.id_proyecto if item.pago_gestiona_fundacion else None
                    editar_hotel.budget_item_id = item.id_rubro if item.pago_gestiona_fundacion else None
                    db.commit()
                else:
                    logging.warning(f"Hotel with id {item.id_viaje_hotel} not found for viaje {viaje_id}")
        
        hotel_viaje = ViajesHotelRepository.listar_hoteles_por_viaje(viaje_id, db)
        hoteles_ids = {m.travel_accommodation_id for m in hotel_viaje}

        hoteles_list_ids = {hotel.id_viaje_hotel for hotel in hotelList}
        hotel_a_eliminar = []
        if validar_eliminacion:
            hotel_a_eliminar = hoteles_ids - hoteles_list_ids

        for id_viaje_hotel in hotel_a_eliminar:
            # Eliminar el hotel de la base de datos
            db.query(TravelAccommodations).filter(TravelAccommodations.travel_accommodation_id == id_viaje_hotel).delete()
            logging.info(f"El hotel {id_viaje_hotel} ha sido eliminado para el viaje {viaje_id}")
        db.commit()
    except Exception as e:
        logging.error(f"Failed to update hotel for viaje {viaje_id}: {str(e)}")
        raise PruebaCreationError(str(e))



def obtener_viaje_por_id(guuid: str, db: Session) -> ViajesCreate:
    viajeDb = ViajesRepository.obtener_por_guid(guuid, db)
    itinerario = ViajesItinerarioRepository.listar_itinerarios_por_viaje(viajeDb.travel_request_id, db)
    hoteles = ViajesHotelRepository.listar_hoteles_por_viaje(viajeDb.travel_request_id, db)
    viajeDTO = viajeCreateDTO(viajeDb, itinerario, hoteles, db)

    return viajeDTO

def viajeCreateDTO(viajeDb: TravelRequests, itinerario: list[TravelItineraries], hoteles: list[TravelAccommodations], db: Session) -> ViajesCreate:
    viajeDTO = ViajesCreate(
        id_viaje=viajeDb.travel_request_id,
        guid=viajeDb.guid,
        id_categoria=viajeDb.travel_request_id,
        codigo=viajeDb.code,
        objetivo_actividad=viajeDb.activity_purpose,
        fecha_inicio_viaje=viajeDb.travel_start_date,
        fecha_fin_viaje=viajeDb.travel_end_date,
        requiere_anticipo=viajeDb.requires_advance_payment,
        fecha_solicitud=viajeDb.created_at.date() if viajeDb.created_at else None,
        requiere_tiquetes=viajeDb.requires_tickets,
        id_supervisor_aprueba=viajeDb.supervisor_user_id,
        id_rol_aprobacion_supervisor=viajeDb.supervisor_approval_role_id,
        itinerario = [],
        hotel = [],
        guid_msft=viajeDb.user.guid_msft if viajeDb.user else None,
        id_estado=viajeDb.travel_status_id,
        observaciones_adicionales=viajeDb.additional_comments,
        menciones_json=viajeDb.mentions_json,
        id_usuarios_mencion=viajeDb.mentioned_user_ids,
        usuario=viajeDb.user.full_name if viajeDb.user else None,
        id_solicitud_aprobacion=viajeDb.approval_request_id,
        es_invitado=viajeDb.is_guest,
        persona_invitada=viajeDb.guest_name,
        documento_persona_invitada=viajeDb.guest_document,
        telefono_persona_invitada=viajeDb.guest_phone,
        correo_persona_invitada=viajeDb.guest_email if viajeDb.is_guest else viajeDb.user.email if viajeDb.user else None,
        id_solicitud_aprobacion_legalizacion=viajeDb.expense_approval_request_id,
        viaje_internacional=viajeDb.is_international,
        pais=viajeDb.country if viajeDb.country else None,
        id_programa=viajeDb.program_id,
        estado=viajeDb.travel_status.name if viajeDb.travel_status else None,
        motivo_anulo=None,
        fecha_anulo=None,
        objetivo=viajeDb.activity_purpose,
        rubro_corto=viajeDb.short_rubro,
        actividad=f"{viajeDb.activity.code} - {viajeDb.activity.description}" if viajeDb.activity else None,
        rubro=viajeDb.rubro.rubros if viajeDb.rubro else None,
        anio_rubro=viajeDb.year_rubro,
        id_rubro=viajeDb.rubro_id,
        id_actividad=viajeDb.activity_id,
        contacto_emergencia=viajeDb.emergency_contact,
        telefono_emergencia=viajeDb.emergency_phone,
        parentesco_emergencia=viajeDb.emergency_relationship,
        fecha_nacimiento_viajero=viajeDb.traveler_birth_date,
    )
    for it in itinerario:
        viajeDTO.itinerario.append(
            ViajesItinerarioBase(
                departamento_origen=it.origin_municipality.region.name if it.origin_municipality else None,
                departamento_destino=it.destination_municipality.region.name if it.destination_municipality else None,
                municipio_origen=it.origin_municipality.name if it.origin_municipality else None,
                municipio_destino=it.destination_municipality.name if it.destination_municipality else None,
                id_viaje_itinerario=it.travel_itinerary_id,
                fecha=it.travel_date,
                hora=it.departure_time,
                id_municipio_destino=it.destination_municipality_id,
                id_municipio_origen=it.origin_municipality_id,
                observaciones=it.comments,
                editado=False,
                soporte_tiquetes=it.ticket_support_document,
                id_departamento_origen=it.origin_municipality.region_id if it.origin_municipality else None,
                id_departamento_destino=it.destination_municipality.region_id if it.destination_municipality else None,
                es_zona_rural=it.is_rural_area,
                observaciones_zona_rural=it.rural_area_comments,
                id_viaje=it.travel_request_id,
                soporte_pase_abordar=it.boarding_pass_document,
                ruta_soporte_pase_abordar=it.boarding_pass_path,
                ruta_soporte_tiquetes=it.ticket_support_path,
                requiere_tiquetes_aereos=it.requires_air_tickets,
                id_proyecto=it.project_id,
                id_rubro=it.budget_item_id,
                proyecto=it.project_id,  # Adjust if necessary
                rubro=it.budget_item_id  # Adjust if necessary
            )
        )
    for ht in hoteles:
        viajeDTO.hotel.append(
            ViajesHotelBase(
                fecha_llegada=ht.check_in_date,
                fecha_salida=ht.check_out_date,
                observaciones=ht.comments,
                tipo_alojamiento=ht.accommodation_type,
                departamento=ht.municipality.region.name if ht.municipality else None,
                municipio=ht.municipality.name if ht.municipality else None,
                id_viaje_hotel=ht.travel_accommodation_id,
                soporte=ht.support_document,
                ruta_soporte=ht.support_document_path,
                id_municipio=ht.municipality_id,
                id_departamento=ht.municipality.region_id if ht.municipality else None,
                pago_gestiona_fundacion=ht.foundation_managed_payment,
                id_viaje=ht.travel_request_id,
                id_proyecto=ht.project_id,
                id_rubro=ht.budget_item_id,
                proyecto=ht.project_id,  # Adjust if necessary
                rubro=ht.budget_item_id  # Adjust if necessary
            )
        )
    # if anticipo and not anticipo.pago_rechazado:
    #     detalleAnticipo = AnticiposDetalleRepository.obtener_detalle_anticipo_reintegro(anticipo.id_anticipo, db, False)
    #     soporte_cb = db.query(AnticiposDocumentos).filter(AnticiposDocumentos.id_anticipo == anticipo.id_anticipo, AnticiposDocumentos.id_tipo_documento_anticipo_reintegro == 1).first()
    #     viajeDTO.anticipo = AnticiposReintegrosBase(
    #         id_anticipo=anticipo.id_anticipo,
    #         id_relacion=anticipo.id_relacion,
    #         id_tipo_anticipo=anticipo.id_tipo_anticipo,
    #         codigo=anticipo.codigo,
    #         estado=anticipo.estado,
    #         valor=AnticiposService.obtener_valor_anticipo_reintegro(1, viajeDb.id_viaje, db),
    #         detalle=[],
    #         soporte_pago=anticipo.soporte_pago,
    #         numero_retiros=anticipo.numero_retiros,
    #         gastos_bancarios=anticipo.gastos_bancarios,
    #         rpc=anticipo.rpc,
    #         ruta_rpc=anticipo.ruta_rpc,
    #         documento_contable=anticipo.documento_contable,
    #         ruta_documento_contable=anticipo.ruta_documento_contable,
    #         nombre_tercero=anticipo.nombre_tercero,
    #         id_tipo_cuenta=anticipo.id_tipo_cuenta,
    #         comprobante_egreso=anticipo.comprobante_egreso,
    #         ruta_comprobante_egreso=anticipo.ruta_comprobante_egreso,
    #         documento_consignacion_bancaria=soporte_cb.soporte if soporte_cb else None,
    #         ruta_documento_consignacion_bancaria=soporte_cb.ruta_soporte if soporte_cb else None,
    #         documento_legalizacion=anticipo.documento_legalizacion,
    #         ruta_documento_legalizacion=anticipo.ruta_documento_legalizacion,
    #         documento_soporte=anticipo.documento_soporte,
    #         ruta_documento_soporte=anticipo.ruta_documento_soporte,
    #         diminucion_rpc=anticipo.diminucion_rpc,
    #         ruta_diminucion_rpc=anticipo.ruta_diminucion_rpc,
    #         id_estado=anticipo.id_estado
    #     )
    #     for item in detalleAnticipo:
    #         viajeDTO.anticipo.detalle.append(
    #             AnticiposDetalleBase(
    #                 id_anticipo_detalle=item.id_anticipo_detalle,
    #                 id_concepto=item.id_concepto,
    #                 valor_anticipo=item.valor_anticipo,
    #                 observaciones=item.observaciones,
    #                 concepto=item.concepto.concepto if item.concepto else None,
    #                 id_proyecto=item.id_proyecto,
    #                 id_rubro=item.id_rubro,
    #                 proyecto= item.proyecto.proyecto if item.proyecto else None,
    #                 rubro= item.rubro.rubro if item.rubro else None,
    #                 deshabilitado=item.deshabilitado
    #             )
    #         )
    
    print("Reintegro ------------------")
    # if reintegro or (total_conceptos_pendiente_rubro > 0):
    #     detalle = []
    #     if not reintegro:
    #         viajeDTO.reintegro = deepcopy(viajeDTO.anticipo)
    #         viajeDTO.reintegro.detalle = []
    #         viajeDTO.reintegro.valor = 0
    #         detalle = AnticiposDetalleRepository.obtener_detalle_anticipo_reintegro_items_legalizacion(anticipo.id_anticipo, db, True)
    #     else:
    #         detalle = AnticiposDetalleRepository.obtener_detalle_anticipo_reintegro(reintegro.id_anticipo, db, True)
    #         viajeDTO.reintegro = AnticiposReintegrosBase(
    #             id_anticipo=reintegro.id_anticipo,
    #             id_relacion=reintegro.id_relacion,
    #             id_tipo_anticipo=reintegro.id_tipo_anticipo,
    #             codigo=reintegro.codigo,
    #             estado=reintegro.estado,
    #             valor=AnticiposService.obtener_valor_anticipo_reintegro(1, viajeDb.id_viaje, db, True),
    #             detalle=[],
    #             soporte_pago=reintegro.soporte_pago,
    #             numero_retiros=reintegro.numero_retiros,
    #             gastos_bancarios=reintegro.gastos_bancarios,
    #             rpc=reintegro.rpc,
    #             ruta_rpc=reintegro.ruta_rpc,
    #             documento_contable=reintegro.documento_contable,
    #             ruta_documento_contable=reintegro.ruta_documento_contable,
    #             nombre_tercero=reintegro.nombre_tercero,
    #             id_tipo_cuenta=reintegro.id_tipo_cuenta,
    #             comprobante_egreso=reintegro.comprobante_egreso,
    #             ruta_comprobante_egreso=reintegro.ruta_comprobante_egreso,
    #             documento_consignacion_bancaria=reintegro.documento_consignacion_bancaria,
    #             documento_soporte=reintegro.documento_soporte,
    #             ruta_documento_soporte=reintegro.ruta_documento_soporte,
    #         )
    #     for item in detalle:
    #         viajeDTO.reintegro.detalle.append(
    #             AnticiposDetalleBase(
    #                 id_anticipo_detalle=item.id_anticipo_detalle,
    #                 id_concepto=item.id_concepto,
    #                 valor_anticipo=item.valor_anticipo,
    #                 observaciones=item.observaciones,
    #                 concepto=item.concepto.concepto if item.concepto else None,
    #                 id_proyecto=item.id_proyecto,
    #                 id_rubro=item.id_rubro,
    #                 proyecto= item.proyecto.proyecto if item.proyecto else None,
    #                 rubro= item.rubro.rubro if item.rubro else None,
    #             )
    #         )

    return viajeDTO


def procesar_accion_solicitud_aprobacion(accion: AccionSolicitudAprobacion, usuario_guid: str, id_categoria: int, db: Session, background_tasks: BackgroundTasks) -> ResponseRequest:
    try:
        usuario = UsuariosRepository.obtener_por_guid_msft(usuario_guid.strip(), db)
        if not usuario:
            raise PruebaNotFoundError("Usuario no encontrado")

        
        # if accion.tipo_accion == "SOLICITUD_AJUSTADA" and usuario_guid.strip() == str(accion.viaje.guid_msft) and accion.tipo_solicitud == "SV":
        #     actualizar_viaje(accion.viaje.guid, accion.viaje, db, usuario_guid, background_tasks, False)
        
        respuesta = SolicitudesAprobacionService.actualizar_ruta(accion, id_categoria, usuario.id, db, accion.viaje.id_supervisor_aprueba, accion.viaje.id_viaje)
        if respuesta.solicitud_exitosa:
            viaje = ViajesRepository.obtener_por_guid_id_solicitud_aprobacion(accion.viaje.guid, accion.id_solicitud_aprobacion, db)
            
            itinerario = ViajesItinerarioRepository.listar_itinerarios_por_viaje(viaje.travel_request_id, db)
            hoteles = ViajesHotelRepository.listar_hoteles_por_viaje(viaje.travel_request_id, db)
            # anticipos = AnticiposDetalleRepository.listar_anticipos_por_viaje(viajeDb.id_viaje, db)
            
            notificacion_pagos = False
            destinatarios = []
            historialAprobacionSolicitud = []
            historialAprobacionSolicitud = SolicitudesAprobacionService.obtener_solicitud_aprobacion_por_id_asociado_id_categoria(viaje.travel_request_id, id_categoria, db)
            if accion.tipo_solicitud == CATEGORIA_APROBACION_SOLICITUD_VIAJE:
                viaje.travel_status_id = 4 if respuesta.mensaje == "RUTA_COMPLETA" else 2 if respuesta.mensaje == "EN_PROCESO" else 3 if respuesta.mensaje == "AJUSTES" else viaje.travel_status_id

                
                
               
                
                destinatarios.append(usuario.email)

               
                # if viaje.travel_status_id == 3:
                #     destinatarios.append(viaje.user.email)
                # else:
                #     emailUsuariosRuta = SolicitudesAprobacionService.obtener_usuarios_ruta(viaje.approval_request_id, db, viaje.supervisor_user_id)
                #     for email in emailUsuariosRuta:
                #         destinatarios.append(email)

                # if accion.id_usuarios_mencion:
                #     usuariosNotificacion = UsuariosRepository.obtener_por_ids(accion.id_usuarios_mencion, db)
                #     for usuario in usuariosNotificacion:
                #         if usuario.email not in destinatarios:
                #             destinatarios.append(usuario.email)
                    
                    # notificacion_pagos = SolicitudesAprobacionService.validar_solicitud_para_pago(viaje.id_solicitud_aprobacion, db, viaje.id_supervisor_aprueba)
                # mensaje = f"Anticipo disponible para pago asociado a la solicitud de viaje {viaje.code}" if notificacion_pagos and pago_realizado == False else f"El anticipo asociado a la solicitud de viaje {viaje.code} ha sido pagado" if notificacion_pagos and pago_realizado else f"Solicitud de viaje {viaje.code} enviada por aprobación" if viaje.id_estado_solicitud == 2 else f"Solicitud de viaje {viaje.code} aprobada" if viaje.id_estado_solicitud == 4 else f"Solicitud de viaje {viaje.code} requerimiento de ajustes" if viaje.id_estado_solicitud == 3 else ""
                # # mensaje = f"Solicitud de viaje {viaje.codigo} enviada por aprobación" if viaje.id_estado_solicitud == 2 else f"Solicitud de viaje {viaje.codigo} aprobada" if viaje.id_estado_solicitud == 4 else f"Solicitud de viaje {viaje.codigo} requerimiento de ajustes" if viaje.id_estado_solicitud == 3 else ""
               
                # to_recipients = [{"emailAddress": {"address": correo}} for correo in destinatarios]

                # print("Destinatarios:", to_recipients)
                # print("mensaje", mensaje)

                

                



            # if id_categoria == 2:
            #     accion.viaje.enviar_aprobacion = False
            #     # if(viaje.id_viajero == usuario.id_usuario and (accion.orden_actual == 1 or accion.orden_actual is None)):
            #     #     guardar_legalizacion(accion.viaje, db)
            #     viaje.travel_status_id = 7 if respuesta.mensaje == "RUTA_COMPLETA" else 5 if respuesta.mensaje == "EN_PROCESO" else 6 if respuesta.mensaje == "AJUSTES" else viaje.travel_status_id
            #     # if accion.asigna_presupuesto_viajes:
            #     #     for anticipo in accion.viaje.reintegro.detalle:
            #     #         # anticipo_detalle_db = db.query(Anticipos).filter(
            #     #         #     Anticipos.id_anticipo == anticipo.id_anticipo,
            #     #         #     Anticipos.id_relacion == viaje.id_viaje
            #     #         # ).first()
            #     #         anticipo_detalle_db = AnticiposService.obtener_detalle_anticipo_por_id(anticipo.id_anticipo_detalle, db)
            #     #         if anticipo_detalle_db:
            #     #             anticipo_detalle_db.id_proyecto = anticipo.id_proyecto
            #     #             anticipo_detalle_db.id_rubro = anticipo.id_rubro
            #     #             db.commit()
            #     #             db.refresh(anticipo_detalle_db)
                
            #     notificacion_pagos = False
            #     pago_realizado = False

            # #     if accion.agrega_documento_contable:
            # #         if accion.viaje.reintegro.documento_contable:
            # #             AnticiposService.actualizaEstadoAnticipo(accion.viaje.reintegro.id_anticipo, 2, db, True, True, usuario_guid)
            # #             notificacion_pagos = True

            # #     if accion.habilitar_pago and viaje.id_estado_solicitud == 5:
            # #         AnticiposService.actualizaEstadoAnticipo(accion.viaje.reintegro.id_anticipo, 3, db)
            # #         pago_realizado = True
            # #         notificacion_pagos = True
                
            # #     historialAprobacionSolicitud = SolicitudesAprobacionService.obtener_solicitud_aprobacion_por_id_asociado_id_categoria(viaje.id_viaje, 2, db)
                
               
                
            # #     destinatarios.append(usuario.correo)

               
            # #     if viaje.id_estado_solicitud == 6:
            # #         destinatarios.append(viaje.usuario.correo)
            # #     else:
            # #         emailUsuariosRuta = SolicitudesAprobacionService.obtener_usuarios_ruta(viaje.id_solicitud_aprobacion_legalizacion, db, viaje.id_supervisor_aprueba)
            # #         for email in emailUsuariosRuta:
            # #             destinatarios.append(email)
                    
            # #         # notificacion_pagos = SolicitudesAprobacionService.validar_solicitud_para_pago(viaje.id_solicitud_aprobacion, db, viaje.id_supervisor_aprueba)
            # #     # mensaje = f"Anticipo disponible para pago asociado a la solicitud de viaje {viaje.codigo}" if notificacion_pagos else f"Solicitud de viaje {viaje.codigo} enviada por aprobación" if viaje.id_estado_solicitud == 2 else f"Solicitud de viaje {viaje.codigo} aprobada" if viaje.id_estado_solicitud == 4 else f"Solicitud de viaje {viaje.codigo} requerimiento de ajustes" if viaje.id_estado_solicitud == 3 else ""
            # #     # mensaje = f"Solicitud de viaje {viaje.codigo} enviada por aprobación" if viaje.id_estado_solicitud == 2 else f"Solicitud de viaje {viaje.codigo} aprobada" if viaje.id_estado_solicitud == 4 else f"Solicitud de viaje {viaje.codigo} requerimiento de ajustes" if viaje.id_estado_solicitud == 3 else ""
               
            # #     to_recipients = [{"emailAddress": {"address": correo}} for correo in destinatarios]

            # #     print("Destinatarios:", to_recipients)

            # #     mensaje = f"Reintegro disponible para pago asociado a la solicitud de viaje {viaje.codigo}" if notificacion_pagos and pago_realizado == False else f"El reintegro asociado a la solicitud de viaje {viaje.codigo} ha sido pagado" if notificacion_pagos and pago_realizado else f"Legalización de viaje {viaje.codigo} enviada por aprobación" if viaje.id_estado_solicitud == 5 else f"Legalización de viaje {viaje.codigo} aprobada" if viaje.id_estado_solicitud == 7 else f"Legalización de viaje {viaje.codigo} requerimiento de ajustes" if viaje.id_estado_solicitud == 6 else ""
            # #     # mensaje = f"Reintegro disponible para pago asociado a la solicitud de viaje {viaje.codigo}" if notificacion_pagos else f"Legalización de viaje {viaje.codigo} enviada por aprobación" if viaje.id_estado_solicitud == 5 else f"Legalización de viaje {viaje.codigo} aprobada" if viaje.id_estado_solicitud == 7 else f"Legalización de viaje {viaje.codigo} requerimiento de ajustes" if viaje.id_estado_solicitud == 6 else ""

            # # anticipo = AnticiposReintegrosRepository.obtener_anticipo_reintegro_por_tipo_y_relacion(1, viaje.id_viaje, False, db)
            # # reintegro = AnticiposReintegrosRepository.obtener_anticipo_reintegro_por_tipo_y_relacion(1, viaje.id_viaje, True, db)
            # # viajeDTO = viajeCreateDTO(viaje, itinerario, hoteles, anticipo, reintegro, db)

            # # env = Environment(loader=FileSystemLoader(''))
            # # template = env.get_template('templates/notificacion_sv.html')
            # # html_out = template.render(**vars(viajeDTO), 
            # # historialAprobacionSolicitud=historialAprobacionSolicitud)
            # # print("mensaje: XXX : ", mensaje)
            # # background_tasks.add_task(
            # #     NotificacionesService.solicitud_viaje,
            # #     mensaje,
            # #     to_recipients,
            # #     html_out,
            # #     "",
            # #     "",
            # #     db
            # # )
            # # NotificacionesService.solicitud_viaje(mensaje, to_recipients, html_out, "", "", db)

            db.commit()
        return respuesta
    except Exception as e:
        logging.error(f"Failed to process accion solicitud aprobacion: {str(e)}")
        return ResponseRequest(
            solicitud_exitosa=False,
            mensaje=str(e)
        )   




def listar_viajes_por_usuario_sp(
        db: Session, 
        usuario_guid: str, 
        page: int, filtro: str, 
        estado: list[int], 
        fechaDesde: str, 
        fechaHasta: str,
        programa: int = None) -> list[ViajesListSP]:
    try:
        viajes = ViajesRepository.listar_viajes_por_usuario_sp(usuario_guid, db, page, estado, filtro, fechaDesde, fechaHasta, programa)
        valor_gastos_bancarios = 0.0
        for viaje in viajes:
            valor_gastos_bancarios = 0.0  

            viaje.tipo_solicitud_aprobacion = (
                "LV" if viaje.id_solicitud_aprobacion_legalizacion
                else "SV" if viaje.id_solicitud_aprobacion
                else None
            )

            # if viaje.requiere_anticipo and not viaje.pago_anticipo_rechazado:
            #     viaje.valor_anticipo = AnticiposService.obtener_valor_anticipo_reintegro(
            #         1, viaje.id_viaje, db, False
            #     )

            #     anticipo = AnticiposReintegrosRepository.obtener_anticipo_reintegro_por_tipo_y_relacion(
            #         1, viaje.id_viaje, False, db
            #     )

            #     valor_gastos_bancarios = anticipo.gastos_bancarios or 0.0 if anticipo else 0.0
            # else:
            #     viaje.valor_anticipo = 0.0
            
            
            # valor_reintegro = AnticiposService.obtener_valor_anticipo_reintegro(1, viaje.id_viaje, db, True)
            viaje.valor_reintegro = 0.0
            # if valor_reintegro > viaje.valor_anticipo:
            # valor_facturas = AnticiposService.obtener_valor_facturas_reintegro(1, viaje.id_viaje, db)

            # relaciones_facturas = db.query(VWRelacionAnticipoFacturas).filter(
            #     VWRelacionAnticipoFacturas.id_relacion == viaje.id_viaje,
            #     VWRelacionAnticipoFacturas.id_tipo_anticipo == 1
            # ).all()

            # valor_facturas = db.query(
            #     func.coalesce(func.sum(VWRelacionAnticipoFacturas.valor_factura), 0)
            # ).filter(
            #     VWRelacionAnticipoFacturas.id_relacion == viaje.id_viaje,
            #     VWRelacionAnticipoFacturas.id_tipo_anticipo == 1
            # ).scalar()
                
            # viaje.valor_reintegro = Decimal(valor_facturas) - Decimal(viaje.valor_anticipo) + Decimal(valor_gastos_bancarios) if valor_facturas and Decimal(valor_facturas) > (Decimal(viaje.valor_anticipo) - Decimal(valor_gastos_bancarios)) else Decimal(0.0)
        return viajes
    except Exception as e:
        logging.error(f"Failed to list viajes: {str(e)}")
        raise PruebaNotFoundError(str(e))


def lista_generica_lista_viajes(db: Session) -> list[Listados]:
    try:
        programas = ProgramsRepository.listar(db)
        estado_viaje = db.query(TravelStatus).all()
        

        listados = []
        lista_catalogos = []

        #Listado de estados de viaje
        for p in estado_viaje:
            lista_catalogos.append(
                ListaGenerica(
                    identity=p.status_id,
                    valor=p.name,
                    idrelacion=None,
                    valorNumerico=None,
                    valor_referencia=None
                )
            )
        
        listados.append(
            Listados(
                id_listado=0, 
                tipo_listado="Estado viaje", 
                lista_generica=lista_catalogos
            )
        )
        #Listado de programas
        lista_catalogos = []
        for p in programas:
            lista_catalogos.append(
                ListaGenerica(
                    identity=p.id,
                    valor=p.name,
                    idrelacion=None,
                    valorNumerico=None,
                    valor_referencia=None
                )
            )
        
        listados.append(
            Listados(
                id_listado=1,
                tipo_listado="Programas",
                lista_generica=lista_catalogos
            )
        )

        return listados
    except Exception as e:
        logging.error(f"Failed to list: {str(e)}")
        raise PruebaCreationError(str(e))
    


def lista_generica(db: Session, usuario_guid: str) -> list[Listados]:
    try:
        usuario = UsuariosRepository.obtener_por_guid_msft(usuario_guid, db)
        anio = datetime.now().year
        if not usuario:
            return None
        departamentos = RegionsRepository.listar_departamentos(db)
        municipios = RegionsRepository.listar_municipios(db)
        tipo_cuenta = TipoCuentaRepository.listar(db)
        entidades_bancarias = EntidadBancariaRepository.listar(db)
        conceptos_anticipos = ConceptoAnticiposRepository.listar(db)
        supervisor = RoleApprovalSupervisorUsersRepository.listar(db)
        programas = UsersProgramsRepository.listar_programas_por_usuario(int(usuario.id), db)
        usuarios = UsuariosRepository.listar(db)
        rubros = RubrosRepository.listar_rubros_sp(str(anio), db)
        # usuario = UsuariosRepository.obtener_por_guid_msft(usuario_guid.strip(), db)
        listados = []
        lista_catalogos = []

        #Listado de departamentos
        for p in departamentos:
            lista_catalogos.append(
                ListaGenerica(
                    identity=p.id,
                    valor=p.name,
                    idrelacion=None,
                    valorNumerico=None,
                    valor_referencia=None
                )
            )
        
        listados.append(
            Listados(
                id_listado=0, 
                tipo_listado="Departamentos", 
                lista_generica=lista_catalogos
            )
        )

        #Listado de municipios
        lista_catalogos = []
        for p in municipios:
            lista_catalogos.append(
                ListaGenerica(
                    identity=p.id,
                    valor=p.name,
                    idrelacion=p.region_id,
                    valorNumerico=None
                )
            )
        
        listados.append(
            Listados(
                id_listado=1,
                tipo_listado="Municipios",
                lista_generica=lista_catalogos
            )
        )
        #Listado de tipos de cuenta
        lista_catalogos = []
        for p in tipo_cuenta:
            lista_catalogos.append(
                ListaGenerica(
                    identity=p.account_type_id,
                    valor=p.account_type,
                    idrelacion=None,
                    valorNumerico=None,
                    valor_referencia=None
                )
            )

        listados.append(
            Listados(
                id_listado=2,
                tipo_listado="Tipos de Cuenta",
                lista_generica=lista_catalogos
            )
        )

        #Listado de entidades bancarias
        lista_catalogos = []
        for p in entidades_bancarias:
            lista_catalogos.append(
                ListaGenerica(
                    identity=p.bank_id,
                    valor=p.bank,
                    idrelacion=None,
                    valorNumerico=None,
                    valor_referencia=None
                )
            )

        listados.append(
            Listados(
                id_listado=3,
                tipo_listado="Entidades Bancarias",
                lista_generica=lista_catalogos
            )
        )

        #Listado de conceptos anticipos
        lista_catalogos = []
        for p in conceptos_anticipos:
            lista_catalogos.append(
                ListaGenerica(
                    identity=p.expense_advance_concept_id,
                    valor=p.concept,
                    idrelacion=None,
                    valor_referencia=None
                )
            )

        listados.append(
            Listados(
                id_listado=4,
                tipo_listado="Conceptos Anticipos",
                lista_generica=lista_catalogos
            )
        )

        #Supervisores
        lista_catalogos = []
        for p in supervisor:
            lista_catalogos.append(
                ListaGenerica(
                    identity=p.approval_role_id,
                    valor=p.user_name,
                    idrelacion=p.user_id,
                    valorNumerico=None,
                    valor_referencia=None
                )
            )
        
        listados.append(
            Listados(
                id_listado=5,
                tipo_listado="Supervisores",
                lista_generica=lista_catalogos
            )
        )

        #Programas usuario

        lista_catalogos = []
        for programa in programas:
            lista_catalogos.append(
                ListaGenerica(
                    identity=programa.id,
                    valor=programa.name,
                    idrelacion=None,
                    valorNumerico=None,
                    valor_referencia=None
                )
            )

        listados.append(
            Listados(
                id_listado=6,
                tipo_listado="Programas Usuario",
                lista_generica=lista_catalogos
            )
        )

        #Usuarios
        lista_catalogos = []
        for usuario in usuarios:
            lista_catalogos.append(
                ListaGenerica(
                    identity=usuario.id,
                    valor=f"{usuario.first_name} {usuario.other_name} {usuario.last_name} {usuario.other_last_name}",
                    idrelacion=None,
                    valorNumerico=None,
                    valor_referencia=None
                )
            )

        listados.append(
            Listados(
                id_listado=7,
                tipo_listado="Usuarios",
                lista_generica=lista_catalogos
            )
        )

        #Rubros
        lista_catalogos = []
        for p in rubros:
            lista_catalogos.append(
                ListaGenerica(
                    identity=p.rubro_id,
                    valor=f"{p.short_rubro} ({p.rubro})",
                    idrelacion=p.activity_id,
                    valorNumerico=anio,
                    valor_referencia=f"{p.activity_code} - {p.activity_description}",
                    valor_referencia2=p.short_rubro
                )
            )

        listados.append(
            Listados(
                id_listado=8,
                tipo_listado="Rubros",
                lista_generica=lista_catalogos
            )
        )



        #Listado de talleres
        # lista_catalogos = []
        # for p in talleres:
        #     lista_catalogos.append(
        #         ListaGenerica(
        #             identity=p.id_taller,
        #             valor_referencia= str(p.guid),
        #             valor=f"{p.codigo} -> {p.nombre_taller}",
        #             idrelacion=None,
        #             valorNumerico=None
        #         )
        #     )

        # listados.append(
        #     Listados(
        #         id_listado=5,
        #         tipo_listado="Talleres",
        #         lista_generica=lista_catalogos
        #     )
        # )
        #Listado de proyectos
        # lista_catalogos = []
        # for p in proyectos:
        #     lista_catalogos.append(
        #         ListaGenerica(
        #             identity=p.id_proyecto,
        #             valor=p.proyecto,
        #             idrelacion=None,
        #             valorNumerico=None,
        #             valor_referencia=None
        #         )
        #     )

        # listados.append(
        #     Listados(
        #         id_listado=6,
        #         tipo_listado="Proyectos",
        #         lista_generica=lista_catalogos
        #     )
        # )
        # #Listado de rubros
        # lista_catalogos = []
        # for p in rubros:
        #     lista_catalogos.append(
        #         ListaGenerica(
        #             identity=p.id_rubro,
        #             valor=f"({p.anio} - {p.codigo}) -> {p.rubro}",
        #             idrelacion=p.id_proyecto,
        #             valorNumerico=None,
        #             valor_referencia=None
        #         )
        #     )
        # listados.append(
        #     Listados(
        #         id_listado=7,
        #         tipo_listado="Rubros",
        #         lista_generica=lista_catalogos
        #     )
        # )
        # #Salario minimo
        # lista_catalogos = []
        # for salario in salarios_minimos:
        #     listados.append(
        #         Listados(
        #             id_listado=8,
        #             tipo_listado="Salarios Mínimos",
        #             lista_generica=[
        #                 ListaGenerica(
        #                     identity=salario.id_salario_minimo,
        #                     valor=None,
        #                     idrelacion=None,
        #                     valorNumerico=salario.salario,
        #                     valor_referencia=None,
        #                     valorNumerico2=salario.anio if salario.anio is not None else None
        #                 )
        #             ]
        #         )
        #     )

        # #Supervisores
        # lista_catalogos = []
        # for p in supervisor:
        #     lista_catalogos.append(
        #         ListaGenerica(
        #             identity=p.id_rol_aprobacion,
        #             valor=p.nombre,
        #             idrelacion=p.id_usuario,
        #             valorNumerico=None,
        #             valor_referencia=None
        #         )
        #     )
        
        # listados.append(
        #     Listados(
        #         id_listado=9,
        #         tipo_listado="Supervisores",
        #         lista_generica=lista_catalogos
        #     )
        # )
        # #Usuarios
        # lista_catalogos = []
        # for p in usuarios:
        #     lista_catalogos.append(
        #         ListaGenerica(
        #             identity=p.id_usuario,
        #             valor=p.nombre,
        #             idrelacion=None,
        #             valorNumerico=None,
        #             valor_referencia=None
        #         )
        #     )
        # listados.append(
        #     Listados(
        #         id_listado=10,
        #         tipo_listado="Usuarios",
        #         lista_generica=lista_catalogos
        #     )
        # )

        # lista_catalogos = []
        # lista_catalogos.append(
        #     ListaGenerica(
        #         aplicaValidacion=usuario.habilitar_solicitud_viaje if usuario.habilitar_solicitud_viaje is not None else False,
        #         valor=None,
        #         idrelacion=None,
        #         valorNumerico=None,
        #         valor_referencia=None
        #     )
        # )
        # lista_catalogos.append(
        #     ListaGenerica(
        #         aplicaValidacion=usuario.permitir_varias_solicitudes_viajes_talleres if usuario.permitir_varias_solicitudes_viajes_talleres is not None else False,
        #         valor=None,
        #         idrelacion=None,
        #         valorNumerico=None,
        #         valor_referencia=None
        #     )
        # )
        # lista_catalogos.append(
        #     ListaGenerica(
        #         aplicaValidacion=usuario.deshabilitar_bloqueo_anticipo if usuario.deshabilitar_bloqueo_anticipo is not None else False,
        #         valor=None,
        #         idrelacion=None,
        #         valorNumerico=None,
        #         valor_referencia=None
        #     )
        # )
        # listados.append(
        #     Listados(
        #         id_listado=11,
        #         tipo_listado="Configuración Usuario",
        #         lista_generica=lista_catalogos
        #     )
        # )
        
        # lista_catalogos = []
        # for p in tipo_documento_administrativo:
        #     lista_catalogos.append(
        #         ListaGenerica(
        #             identity=p.id_tipo_documento,
        #             valor=f"{p.tipo_documento} ({p.abreviacion})",
        #             idrelacion=None,
        #             valorNumerico=None,
        #             valor_referencia=None
        #         )
        #     )
        # listados.append(
        #     Listados(
        #         id_listado=12,
        #         tipo_listado="Tipo Documento Administrativo",
        #         lista_generica=lista_catalogos
        #     )
        # )

        # lista_catalogos = []
        # for p in cuentas_fcds:
        #     lista_catalogos.append(
        #         ListaGenerica(
        #             identity=p.id_tipo_cuenta,
        #             valor=re.sub(r"[-.,]", "", p.numero_cuenta),
        #             idrelacion=None,
        #             valorNumerico=None,
        #             valor_referencia=None
        #         )
        #     )
        # listados.append(
        #     Listados(
        #         id_listado=13,
        #         tipo_listado="Cuentas FCDS",
        #         lista_generica=lista_catalogos
        #     )
        # )

        # lista_catalogos = []
        # for p in otro_tipo_documento_administrativo:
        #     lista_catalogos.append(
        #         ListaGenerica(
        #             identity=p.id_tipo_documento,
        #             valor=p.tipo_documento,
        #             idrelacion=None,
        #             valorNumerico=None,
        #             valor_referencia=None
        #         )
        #     )
        # listados.append(
        #     Listados(
        #         id_listado=14,
        #         tipo_listado="Otro Tipo Documento Administrativo",
        #         lista_generica=lista_catalogos
        #     )
        # )

       

        
        return listados
    except Exception as e:
        logging.error(f"Failed to list: {str(e)}")
        raise PruebaCreationError(str(e))