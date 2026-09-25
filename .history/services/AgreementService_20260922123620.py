import logging
from datetime import date, datetime
from jinja2 import Environment, FileSystemLoader
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

# DTOs
from dto.ResponseRequest import ResponseRequest
from dto.AgreementsDTO import AgreementsCreate, AgreementsListSP, AgreementItemsBase
from entity.agreements import Agreements
from entity.agreement_items import AgreementItems
from entity.users import Users

# Repositorios
from repository import AgreementsRepository, AgreementItemsRepository, UsuariosRepository

# Excepciones
from exceptions import PruebaCreationError, PruebaNotFoundError

# Servicios
from services import SolicitudesAprobacionService, NotificacionesService

CATEGORIA_APROBACION_CONVENIO = "SOL_CONV"


def crear_convenio(convenio: AgreementsCreate, db: Session, usuario_guid: str, background_tasks: BackgroundTasks) -> ResponseRequest:
    respuesta = ResponseRequest(solicitud_exitosa=True)
    try:
        usuario = UsuariosRepository.obtener_por_guid_msft(usuario_guid.strip(), db)
        if not usuario:
            raise PruebaNotFoundError("Usuario no encontrado")

        fecha_actual = date.today()
        consecutivo = AgreementsRepository.numero_convenios(db)
        
        nuevo_convenio = Agreements()
        nuevo_convenio.code = f"C-{fecha_actual.year}-{consecutivo + 1:02d}"
        nuevo_convenio.created_at = datetime.now()
        nuevo_convenio.created_by_user_id = usuario.id
        nuevo_convenio.title = convenio.titulo
        nuevo_convenio.description = convenio.descripcion
        nuevo_convenio.start_date = convenio.fecha_inicio
        nuevo_convenio.end_date = convenio.fecha_fin
        nuevo_convenio.supervisor_user_id = convenio.id_supervisor_aprueba
        nuevo_convenio.supervisor_approval_role_id = convenio.id_rol_aprobacion_supervisor
        nuevo_convenio.program_id = convenio.id_programa
        nuevo_convenio.additional_comments = convenio.observaciones_adicionales

        db.add(nuevo_convenio)
        db.commit()
        db.refresh(nuevo_convenio)

        # Manejo de ítems / detalles asociados
        if convenio.items:
            actualizar_items_convenio(nuevo_convenio.agreement_id, convenio.items, db)

        # Flujo de aprobación opcional
        if convenio.enviar_aprobacion:
            id_categoria_aprobacion = SolicitudesAprobacionService.obtener_categoria_aprobacion(CATEGORIA_APROBACION_CONVENIO, db)
            if not id_categoria_aprobacion:
                raise PruebaCreationError(f"No se encontró la categoría de aprobación {CATEGORIA_APROBACION_CONVENIO}")

            id_solicitud = SolicitudesAprobacionService.crear_solicitud_aprobacion(
                id_categoria_aprobacion, 
                nuevo_convenio.agreement_id, 
                usuario.id, 
                nuevo_convenio.code, 
                db, 
                nuevo_convenio.supervisor_user_id, 
                nuevo_convenio.program_id
            )
            nuevo_convenio.approval_request_id = id_solicitud
            nuevo_convenio.status_id = 2
            db.commit()
            db.refresh(nuevo_convenio)

            # Plantilla e Integración de Notificaciones en Background
            env = Environment(loader=FileSystemLoader(''))
            template = env.get_template('templates/notificacion_convenio.html')
            html_out = template.render(codigo=nuevo_convenio.code, usuario=usuario.first_name)

            destinatarios = []
            if nuevo_convenio.supervisor_user_id:
                supervisor = db.query(Users).filter(Users.id == nuevo_convenio.supervisor_user_id).first()
                if supervisor and supervisor.email:
                    destinatarios.append(supervisor.email)

            to_recipients = [{"emailAddress": {"address": correo}} for correo in destinatarios]
            if to_recipients:
                background_tasks.add_task(
                    NotificacionesService.solicitud_viaje,  # O servicio correspondiente de notificaciones
                    f"Solicitud de Convenio {nuevo_convenio.code} enviada para aprobación",
                    to_recipients,
                    html_out,
                    "",
                    "",
                    db
                )

        respuesta.identity = nuevo_convenio.agreement_id
        respuesta.mensaje = "Convenio creado exitosamente"
        return respuesta

    except Exception as e:
        logging.error(f"Failed to create convenio: {str(e)}")
        return ResponseRequest(
            solicitud_exitosa=False,
            mensaje=str(e)
        )


def actualizar_convenio(guid: str, convenio: AgreementsCreate, db: Session, usuario_guid: str, background_tasks: BackgroundTasks) -> ResponseRequest:
    respuesta = ResponseRequest(solicitud_exitosa=True)
    try:
        usuario = UsuariosRepository.obtener_por_guid_msft(usuario_guid.strip(), db)
        convenio_db = AgreementsRepository.obtener_por_guid(guid.strip(), db)
        if not convenio_db:
            raise PruebaNotFoundError("Convenio no encontrado")

        convenio_db.updated_at = datetime.now()
        convenio_db.updated_by_user_id = usuario.id
        convenio_db.title = convenio.titulo
        convenio_db.description = convenio.descripcion
        convenio_db.start_date = convenio.fecha_inicio
        convenio_db.end_date = convenio.fecha_fin
        convenio_db.supervisor_user_id = convenio.id_supervisor_aprueba
        convenio_db.supervisor_approval_role_id = convenio.id_rol_aprobacion_supervisor
        convenio_db.program_id = convenio.id_programa
        convenio_db.additional_comments = convenio.observaciones_adicionales

        db.commit()
        db.refresh(convenio_db)

        if convenio.items:
            actualizar_items_convenio(convenio_db.agreement_id, convenio.items, db)

        respuesta.identity = convenio_db.agreement_id
        respuesta.mensaje = "Convenio actualizado exitosamente"
        return respuesta

    except Exception as e:
        logging.error(f"Failed to update convenio: {str(e)}")
        return ResponseRequest(
            solicitud_exitosa=False,
            mensaje=str(e)
        )


def actualizar_items_convenio(convenio_id: int, items_list: list[AgreementItemsBase], db: Session, validar_eliminacion: bool = True) -> None:
    try:
        for item in items_list:
            if item.id_convenio_item is None:
                nuevo_item = AgreementItems(
                    agreement_id=convenio_id,
                    description=item.descripcion,
                    amount=item.monto
                )
                db.add(nuevo_item)
                db.commit()
                item.id_convenio_item = nuevo_item.agreement_item_id
            elif item.editado:
                item_db = AgreementItemsRepository.obtener_por_id(item.id_convenio_item, convenio_id, db)
                if item_db:
                    item_db.description = item.descripcion
                    item_db.amount = item.monto
                    db.commit()

        # Detección y eliminación de registros removidos
        items_db = AgreementItemsRepository.listar_por_convenio(convenio_id, db)
        ids_db = {m.agreement_item_id for m in items_db}
        ids_entrada = {item.id_convenio_item for item in items_list if item.id_convenio_item is not None}

        if validar_eliminacion:
            a_eliminar = ids_db - ids_entrada
            if a_eliminar:
                db.query(AgreementItems).filter(AgreementItems.agreement_item_id.in_(a_eliminar)).delete(synchronize_session=False)
                db.commit()

    except Exception as e:
        logging.error(f"Failed to update items for convenio {convenio_id}: {str(e)}")
        raise PruebaCreationError(str(e))


def obtener_convenio_por_id(guid: str, db: Session) -> AgreementsCreate:
    convenio_db = AgreementsRepository.obtener_por_guid(guid, db)
    if not convenio_db:
        raise PruebaNotFoundError("Convenio no encontrado")
        
    items = AgreementItemsRepository.listar_por_convenio(convenio_db.agreement_id, db)
    return convenioCreateDTO(convenio_db, items, db)


def convenioCreateDTO(convenio_db: Agreements, items: list[AgreementItems], db: Session) -> AgreementsCreate:
    return AgreementsCreate(
        id_convenio=convenio_db.agreement_id,
        guid=convenio_db.guid,
        codigo=convenio_db.code,
        titulo=convenio_db.title,
        descripcion=convenio_db.description,
        fecha_inicio=convenio_db.start_date,
        fecha_fin=convenio_db.end_date,
        items=[
            AgreementItemsBase(
                id_convenio_item=i.agreement_item_id,
                descripcion=i.description,
                monto=i.amount
            ) for i in items
        ]
    )