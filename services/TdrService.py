
import logging
import uuid
from dto.TermsReferenceDTO import TermsReferenceCreate
from exceptions import PruebaCreationError
from fastapi import BackgroundTasks
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from dto.ListaGenerica import ListaGenerica
from dto.ListadosDTO import Listados
from dto.ResponseRequest import ResponseRequest
from repository import TdrRepository
from services import SolicitudesAprobacionService, NotificacionesService, FlujosAprobacionService, TdrDocumentService
from repository import UsuariosRepository, UsersProgramsRepository

CATEGORIA_APROBACION = "TDR"

def obtener_campos_tdr(approval_flow_id: int, db: Session):
    return TdrRepository.obtener_campos_tdr(approval_flow_id, db)

def crear_tdr(tdr: TermsReferenceCreate, db: Session, usuario_guid: str, background_tasks: BackgroundTasks) -> ResponseRequest:
    try:
        usuario = UsuariosRepository.obtener_por_guid_msft(usuario_guid.strip(), db)
        response_request = TdrRepository.guardar_tdr(user_id=usuario.id, tdr=tdr, db=db)
        # response_request = ResponseRequest(solicitud_exitosa=True, mensaje="TDR created successfully")
        return response_request
    except Exception as e:
        logging.error(f"Failed to create TDR: {str(e)}")
        raise PruebaCreationError(str(e))

def previsualizar_tdr(tdr: TermsReferenceCreate, db: Session, usuario_guid: str, background_tasks: BackgroundTasks) -> ResponseRequest:
    try:
        flujo_aprobacion = FlujosAprobacionService.obtener_flujo_aprobacion_por_id(tdr.approval_flow_id, db)
        template = flujo_aprobacion.template if flujo_aprobacion else None
        if not template:
            return ResponseRequest(solicitud_exitosa=False, mensaje="El flujo de aprobación no tiene una plantilla configurada")

        identificador = str(tdr.guid) if tdr.guid else str(uuid.uuid4())
        ruta_pdf = TdrDocumentService.generar_tdr_documento(template, tdr.tdr_form or [], identificador)

        return ResponseRequest(
            solicitud_exitosa=True,
            mensaje="Previsualización generada correctamente",
            guid=identificador,
            archivo=str(ruta_pdf),
        )
    except Exception as e:
        logging.error(f"Failed to create TDR: {str(e)}")
        raise PruebaCreationError(str(e))


def lista_generica(db: Session, usuario_guid: str) -> list[Listados]:
    try:
        usuario = UsuariosRepository.obtener_por_guid_msft(usuario_guid, db)
        id_categoria_aprobacion = SolicitudesAprobacionService.obtener_categoria_aprobacion(CATEGORIA_APROBACION, db)
        flujos_aprobacion = FlujosAprobacionService.obtener_flujo_aprobacion_x_categoria(id_categoria_aprobacion, usuario.id, db)
        programas = UsersProgramsRepository.listar_programas_por_usuario(int(usuario.id), db)
        
        listados = []
        lista_catalogos = []

        
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
                id_listado=0,
                tipo_listado="Programas Usuario",
                lista_generica=lista_catalogos
            )
        )

        #Flujos de aprobación
        lista_catalogos = []
        for flujo in flujos_aprobacion:
            lista_catalogos.append(
                ListaGenerica(
                    identity=flujo.approval_flow_id,
                    valor=flujo.name,
                    idrelacion=flujo.program_id,
                    valorNumerico=None,
                    valor_referencia=None
                )
            )

        listados.append(
            Listados(
                id_listado=1,
                tipo_listado="Flujos de aprobación",
                lista_generica=lista_catalogos
            )
        )


        return listados
    except Exception as e:
        logging.error(f"Failed to list: {str(e)}")
        raise PruebaCreationError(str(e))