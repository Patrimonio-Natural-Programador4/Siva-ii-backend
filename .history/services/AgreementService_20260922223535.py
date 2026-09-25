# ***************************************
# 1. AgreementService.py -- 22 Septiembre 2026
# ***************************************

# -----------------------------------------------------------------------------
# BLOQUE 1: Importación de Módulos, Servicios y Repositorios
# -----------------------------------------------------------------------------
# Se importan las dependencias del sistema:
# - Registro de eventos (logging) y manejo de fechas.
# - DTOs para la transferencia de datos de entrada/salida.
# - Entidades SQLAlchemy (ORM) correspondientes a tablas de la BD.
# - Excepciones personalizadas del dominio.
# - Componentes de FastAPI para tareas en segundo plano (BackgroundTasks).
# - Motor de plantillas Jinja2 para renderizar correos HTML.
# - Repositorios de datos y servicios auxiliares (Notificaciones y Aprobaciones).
import logging
from datetime import date, datetime
from dto.AgreementsDTO import AgreementItemsBase, AgreementsCreate, AgreementsListSP
from dto.ResponseRequest import ResponseRequest
from entity.agreements import AgreementItems, Agreements
from entity.users import Users
from exceptions import PruebaCreationError, PruebaNotFoundError
from fastapi import BackgroundTasks
from jinja2 import Environment, FileSystemLoader
from repository import AgreementItemsRepository, AgreementsRepository, UsuariosRepository
from services import NotificacionesService, SolicitudesAprobacionService
from sqlalchemy.orm import Session

# Constante de negocio que define la categoría para el flujo de aprobación de convenios
CATEGORIA_APROBACION_CONVENIO = "SOL_CONV"


# -----------------------------------------------------------------------------
# BLOQUE 2: Creación de Convenio y Gestión de Flujo de Aprobación
# -----------------------------------------------------------------------------
def crear_convenio(
    db: Session,
    convenio: AgreementsCreate,
    usuario_guid: str,
    background_tasks: BackgroundTasks
) -> Agreements:
    """
    Registra un nuevo convenio en la base de datos, genera su código consecutivo,
    sincroniza sus ítems financieros e inicia el proceso de aprobación si corresponde.
    """
    try:
        # 1. Validación de usuario creador mediante su GUID
        usuario = UsuariosRepository.obtener_usuario_por_guid(db, usuario_guid)
        if not usuario:
            raise PruebaNotFoundError("Usuario no encontrado")

        # 2. Generación del código consecutivo del convenio (Formato: C-AAAA-NC)
        ano_actual = datetime.now().year
        total_convenios_ano = db.query(Agreements).filter(
            Agreements.ano_ejecucion == ano_actual
        ).count()
        consecutivo = total_convenios_ano + 1
        codigo_siva = f"C-{ano_actual}-{consecutivo}"

        # 3. Mapeo del DTO a la Entidad Agreements (ORM)
        nuevo_convenio = Agreements(
            codigo_siva=codigo_siva,
            nombre_convenio=convenio.nombre_convenio,
            objeto_acuerdo=convenio.objeto_acuerdo,
            prioridad_acuerdo=convenio.prioridad_acuerdo,
            ano_ejecucion=ano_actual,
            program_id=convenio.program_id,
            supervisor_user_id=convenio.supervisor_user_id,
            type_id=convenio.type_id,
            modality_id=convenio.modality_id,
            created_by_user_id=usuario.id,
            created_at=datetime.now(),
            status_id=1  # Estado inicial registrado por defecto
        )

        db.add(nuevo_convenio)
        db.flush()  # Obtiene el ID generado en BD sin cerrar la transacción

        # 4. Asignación de ítems e imputaciones presupuestales asociadas
        if convenio.items:
            actualizar_items_convenio(db, nuevo_convenio.id, convenio.items)

        # ---------------------------------------------------------------------
        # SUB-BLOQUE 2.1: Integración con SolicitudesAprobacionService
        # ---------------------------------------------------------------------
        # Si la petición incluye la bandera de envío a aprobación, se inicia el flujo:
        if convenio.enviar_aprobacion:
            # a. Obtiene la categoría de aprobación del sistema
            categoria = SolicitudesAprobacionService.obtener_categoria_por_codigo(
                db, CATEGORIA_APROBACION_CONVENIO
            )
            
            # b. Crea el registro de solicitud de aprobación
            solicitud = SolicitudesAprobacionService.crear_solicitud_aprobacion(
                db=db,
                categoria_id=categoria.id,
                entidad_id=nuevo_convenio.id,
                usuario_creador_id=usuario.id
            )

            # c. Actualiza el convenio al estado "Pendiente de Aprobación" y vincula la solicitud
            nuevo_convenio.status_id = 2  
            nuevo_convenio.approval_request_id = solicitud.id

            # d. Notificación por correo electrónico en segundo plano usando Jinja2
            env = Environment(loader=FileSystemLoader("templates"))
            template = env.get_template("notificacion_convenio.html")
            
            # Obtiene el usuario supervisor que debe aprobar
            supervisor = UsuariosRepository.obtener_usuario_por_id(db, convenio.supervisor_user_id)
            
            html_content = template.render(
                nombre_supervisor=f"{supervisor.first_name} {supervisor.last_name}",
                codigo_convenio=codigo_siva,
                nombre_convenio=convenio.nombre_convenio
            )

            # Se encola el envío del correo de notificación
            background_tasks.add_task(
                NotificacionesService.enviar_correo,
                destinatario=supervisor.email,
                asunto=f"Solicitud de Aprobación de Convenio - {codigo_siva}",
                cuerpo_html=html_content
            )

        db.commit()
        db.refresh(nuevo_convenio)
        return nuevo_convenio

    except Exception as e:
        db.rollback()
        logging.error(f"Error al crear el convenio: {str(e)}")
        raise PruebaCreationError(f"Error al procesar la creación del convenio: {str(e)}")


# -----------------------------------------------------------------------------
# BLOQUE 3: Actualización de Convenio Existente
# -----------------------------------------------------------------------------
def actualizar_convenio(
    db: Session,
    convenio_guid: str,
    convenio: AgreementsCreate,
    usuario_guid: str
) -> Agreements:
    """
    Modifica la información general de un convenio existente y 
    reconcilia sus ítems presupuestales.
    """
    try:
        # Validación de usuario y convenio existente
        usuario = UsuariosRepository.obtener_usuario_por_guid(db, usuario_guid)
        convenio_existente = db.query(Agreements).filter(
            Agreements.guid == convenio_guid
        ).first()

        if not convenio_existente:
            raise PruebaNotFoundError("Convenio no encontrado")

        # Actualización de campos de auditoría e información general
        convenio_existente.nombre_convenio = convenio.nombre_convenio
        convenio_existente.objeto_acuerdo = convenio.objeto_acuerdo
        convenio_existente.prioridad_acuerdo = convenio.prioridad_acuerdo
        convenio_existente.program_id = convenio.program_id
        convenio_existente.supervisor_user_id = convenio.supervisor_user_id
        convenio_existente.type_id = convenio.type_id
        convenio_existente.modality_id = convenio.modality_id
        convenio_existente.updated_by_user_id = usuario.id
        convenio_existente.updated_at = datetime.now()

        # Reconciliación de ítems presupuestales
        if convenio.items is not None:
            actualizar_items_convenio(db, convenio_existente.id, convenio.items)

        db.commit()
        db.refresh(convenio_existente)
        return convenio_existente

    except Exception as e:
        db.rollback()
        logging.error(f"Error al actualizar el convenio {convenio_guid}: {str(e)}")
        raise PruebaCreationError(f"Error al actualizar el convenio: {str(e)}")


# -----------------------------------------------------------------------------
# BLOQUE 4: Sincronización y Reconciliación de Ítems (AgreementItems)
# -----------------------------------------------------------------------------
def actualizar_items_convenio(
    db: Session,
    convenio_id: int,
    items: list[AgreementItemsBase]
):
    """
    Realiza la sincronización de ítems (Creación, Edición y Eliminación)
    para un convenio específico.
    """
    # Obtiene los IDs de los ítems registrados actualmente en la BD
    items_actuales = db.query(AgreementItems).filter(
        AgreementItems.agreement_id == convenio_id
    ).all()
    
    ids_actuales = {item.id for item in items_actuales}
    ids_recibidos = {item.id_convenio_item for item in items if item.id_convenio_item is not None}

    # 1. ELIMINACIÓN: Elimina ítems que estaban en la BD pero no llegaron en la nueva lista
    ids_a_eliminar = ids_actuales - ids_recibidos
    if ids_a_eliminar:
        db.query(AgreementItems).filter(
            AgreementItems.id.in_(ids_a_eliminar)
        ).delete(synchronize_session=False)

    # 2. CREACIÓN O EDICIÓN: Recorre la lista enviada para procesar cada ítem
    for item in items:
        if item.id_convenio_item is None:
            # Creación de nuevo ítem
            nuevo_item = AgreementItems(
                agreement_id=convenio_id,
                descripcion=item.descripcion,
                monto=item.monto
            )
            db.add(nuevo_item)
        else:
            # Modificación si viene marcado con la bandera 'editado'
            if getattr(item, 'editado', False):
                item_db = db.query(AgreementItems).filter(
                    AgreementItems.id == item.id_convenio_item
                ).first()
                if item_db:
                    item_db.descripcion = item.descripcion
                    item_db.monto = item.monto


# -----------------------------------------------------------------------------
# BLOQUE 5: Consultas y Conversión a DTOs
# -----------------------------------------------------------------------------
def obtener_convenio_por_id(db: Session, convenio_guid: str) -> dict:
    """
    Recupera la información completa de un convenio por su GUID 
    y construye el diccionario/DTO detallado de respuesta.
    """
    convenio = db.query(Agreements).filter(Agreements.guid == convenio_guid).first()
    if not convenio:
        raise PruebaNotFoundError("Convenio no encontrado")

    # Mapeo de ítems asociados
    items_dto = [
        AgreementItemsBase(
            id_convenio_item=item.id,
            descripcion=item.descripcion,
            monto=item.monto
        ) for item in convenio.items
    ]

    return {
        "guid": convenio.guid,
        "codigo_siva": convenio.codigo_siva,
        "nombre_convenio": convenio.nombre_convenio,
        "objeto_acuerdo": convenio.objeto_acuerdo,
        "prioridad_acuerdo": convenio.prioridad_acuerdo,
        "program_id": convenio.program_id,
        "supervisor_user_id": convenio.supervisor_user_id,
        "type_id": convenio.type_id,
        "modality_id": convenio.modality_id,
        "items": items_dto
    }
    
    
