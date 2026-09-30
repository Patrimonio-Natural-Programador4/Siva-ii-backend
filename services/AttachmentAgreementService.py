import os
import re
import base64
import logging
from datetime import datetime
from pathlib import Path
from sqlalchemy.orm import Session
from repository import AttachmentAgreementRepository

from entity.attachment_agreement import Attachment_Agreement

logger = logging.getLogger(__name__)

# Directorio base de soportes, relativo a la raíz del proyecto backend
BASE_DIR = Path(__file__).parent.parent
ASSESSMENTS_DIR = BASE_DIR / "soportes" / "acuerdos" / "evaluacion_capacidades"

# Tamaño máximo permitido para el archivo Excel (10 MB)
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024

# Extensión permitida
ALLOWED_EXTENSIONS = [".pdf"]

# Magic bytes para archivos PDF
PDF_MAGIC_BYTES = b'%PDF'


def _decodificar_base64(base64_data: str) -> bytes:
    if "," in base64_data:
        base64_data = base64_data.split(",", 1)[1]
    return base64.b64decode(base64_data)


def _validar_contenido(file_bytes: bytes) -> bool:
    if len(file_bytes) < 4:
        return False
    return file_bytes[:4] == PDF_MAGIC_BYTES


def _sanitizar_codigo_evaluacion(codigo_evaluacion_capacidad: str) -> str:
    sanitized = "".join(c for c in codigo_evaluacion_capacidad if c.isalnum() or c == "-")
    if not sanitized:
        raise ValueError("Código de evaluacion de capacidad inválido después de sanitización")
    return sanitized


def guardar_documento_evaluacion_capacidad(
    codigo_evaluacion_capacidad: str,
    base64_data: str,
    db: Session,
    capacity_assessments_id: int,
    nombre_original: str | None = None,
    documents_types_agreements_id: int | None = None,
    observaciones: str | None = None
) -> str:
    # Decodificar el contenido Base64
    try:
        file_bytes = _decodificar_base64(base64_data)
    except Exception as e:
        raise ValueError(f"Error al decodificar el archivo Base64: {e}")

    # Validar tamaño del archivo
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise ValueError(
            f"El archivo excede el tamaño máximo permitido de {MAX_FILE_SIZE_BYTES // (1024 * 1024)} MB"
        )

    # Validar contenido (magic bytes)
    if not _validar_contenido(file_bytes):
        raise ValueError("El archivo no es un archivo PDF válido")

    # Sanitizar código del viaje para nombre de carpeta
    codigo_sanitizado = _sanitizar_codigo_evaluacion(codigo_evaluacion_capacidad)

    # Construir ruta de la carpeta del viaje
    carpeta_evaluacion_capacidad = ASSESSMENTS_DIR / codigo_sanitizado

    # Validar que la ruta resuelta no escape del directorio base (prevención path traversal)
    carpeta_resuelta = carpeta_evaluacion_capacidad.resolve()
    evaluacion_capacidad_resuelta = ASSESSMENTS_DIR.resolve()
    if not str(carpeta_resuelta).startswith(str(evaluacion_capacidad_resuelta) + os.sep):
        raise ValueError("Ruta de destino inválida")

    # Crear carpeta si no existe
    carpeta_evaluacion_capacidad.mkdir(parents=True, exist_ok=True)

    # Generar nombre del archivo con nueva convención
    fecha_hora = datetime.now().strftime("%Y%m%d%H%M")
    
    if not nombre_original:
        nombre_base = "DOCUMENTO_EVALUACION"
        extension = ".pdf"
    else:
        nombre_original_base, extension = os.path.splitext(nombre_original)
        nombre_base = nombre_original_base.upper()
        nombre_base = "".join(c if c.isalnum() else "_" for c in nombre_base)
        # Quitar la redundancia de fecha previa si la hay
        nombre_base = re.sub(r'_+[\d_]+$', '', nombre_base)

    if extension.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Extensión de archivo {extension} no permitida")

    prefijo = ""
    if documents_types_agreements_id == 1:
        prefijo = "EVA_CAP"  # PREFIJO QUE LLEVARA EL ARCHIVOOOOOOOOOO
    elif documents_types_agreements_id == 2:
        prefijo = "DRELACIONADO"

    nombre_archivo = f"{prefijo}{fecha_hora}{extension.lower()}"
    ruta_archivo = carpeta_evaluacion_capacidad / nombre_archivo

    # Escribir archivo en disco
    ruta_archivo.write_bytes(file_bytes)
    logger.info(f"Archivo guardado: {ruta_archivo}")

    # Registrar en BD a través del repositorio (sin sobreescribir los anteriores)
    AttachmentAgreementRepository.save_attachment_agreement(
        capacity_assessments_id=capacity_assessments_id,
        attachment_name=nombre_archivo,
        path_document=str(ruta_archivo),
        db=db,
        documents_types_agreements_id=documents_types_agreements_id,
        observations=observaciones
    )
    logger.info(f"Registro de archivo creado en BD para evaluación de capacidad {codigo_evaluacion_capacidad}: {nombre_archivo}")

    return nombre_archivo


def obtener_nombre_archivo_evaluacion_capacidad(capacity_assessments_id: int, db: Session) -> str | None:
    registro = AttachmentAgreementRepository.get_attachment_agreement_by_capacity_assessments_id(capacity_assessments_id, db)
    if registro:
        return registro.attachment_name
    return None


def obtener_path_document_evaluacion_capacidad(capacity_assessments_id: int, db: Session) -> str | None:
    registro = AttachmentAgreementRepository.get_attachment_agreement_by_capacity_assessments_id(capacity_assessments_id, db)
    if registro:
        return registro.path_document
    return None


def listar_nombres_archivos_evaluacion_capacidad(capacity_assessments_id: int, db: Session) -> list[Attachment_Agreement]:
    registros = AttachmentAgreementRepository.list_attachment_agreement_by_capacity_assessments_id(capacity_assessments_id, db)
    return [r.attachment_name for r in registros if r.attachment_name]

