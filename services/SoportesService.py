import os
import base64
import logging
from datetime import datetime
from pathlib import Path
from sqlalchemy.orm import Session
from repository import SoportesRepository

logger = logging.getLogger(__name__)

# Directorio base de soportes, relativo a la raíz del proyecto backend
BASE_DIR = Path(__file__).parent.parent
SOPORTES_DIR = BASE_DIR / "soportes" / "administrativo" / "viajes"

# Tamaño máximo permitido para el archivo Excel (10 MB)
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024

# Extensión permitida
ALLOWED_EXTENSION = ".xlsx"

# Magic bytes para archivos XLSX (ZIP/PK header)
XLSX_MAGIC_BYTES = b'\x50\x4b\x03\x04'


def _decodificar_base64(base64_data: str) -> bytes:
    if "," in base64_data:
        base64_data = base64_data.split(",", 1)[1]
    return base64.b64decode(base64_data)


def _validar_contenido_xlsx(file_bytes: bytes) -> bool:
    if len(file_bytes) < 4:
        return False
    return file_bytes[:4] == XLSX_MAGIC_BYTES


def _sanitizar_codigo_viaje(codigo_viaje: str) -> str:
    sanitized = "".join(c for c in codigo_viaje if c.isalnum() or c == "-")
    if not sanitized:
        raise ValueError("Código de viaje inválido después de sanitización")
    return sanitized


def guardar_excel_viaje(
    codigo_viaje: str,
    base64_data: str,
    db: Session,
    travel_request_id: int
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
    if not _validar_contenido_xlsx(file_bytes):
        raise ValueError("El archivo no es un archivo XLSX válido")

    # Sanitizar código del viaje para nombre de carpeta
    codigo_sanitizado = _sanitizar_codigo_viaje(codigo_viaje)

    # Construir ruta de la carpeta del viaje
    carpeta_viaje = SOPORTES_DIR / codigo_sanitizado

    # Validar que la ruta resuelta no escape del directorio base (prevención path traversal)
    carpeta_resuelta = carpeta_viaje.resolve()
    soportes_resuelta = SOPORTES_DIR.resolve()
    if not str(carpeta_resuelta).startswith(str(soportes_resuelta) + os.sep):
        raise ValueError("Ruta de destino inválida")

    # Crear carpeta si no existe
    carpeta_viaje.mkdir(parents=True, exist_ok=True)

    # Generar nombre del archivo con fecha y hora (Año-Mes-Día_Hora-Minuto) para trazabilidad
    fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M")
    nombre_archivo = f"listado_invitados_{fecha_hora}{ALLOWED_EXTENSION}"
    ruta_archivo = carpeta_viaje / nombre_archivo

    # Escribir archivo en disco
    ruta_archivo.write_bytes(file_bytes)
    logger.info(f"Archivo guardado: {ruta_archivo}")

    # Registrar en BD a través del repositorio (sin sobreescribir los anteriores)
    SoportesRepository.guardar_soporte(
        travel_request_id=travel_request_id,
        nombre_archivo=nombre_archivo,
        ruta_archivo=str(ruta_archivo),
        db=db
    )
    logger.info(f"Registro de archivo creado en BD para viaje {codigo_viaje}: {nombre_archivo}")

    return nombre_archivo


def obtener_nombre_archivo_viaje(travel_request_id: int, db: Session) -> str | None:
    registro = SoportesRepository.obtener_soporte_por_travel_request_id(travel_request_id, db)
    if registro:
        return registro.attachment_name
    return None


def obtener_path_document_viaje(travel_request_id: int, db: Session) -> str | None:
    registro = SoportesRepository.obtener_soporte_por_travel_request_id(travel_request_id, db)
    if registro:
        return registro.path_document
    return None


def listar_nombres_archivos_viaje(travel_request_id: int, db: Session) -> list[str]:
    registros = SoportesRepository.listar_soportes_por_travel_request_id(travel_request_id, db)
    return [r.attachment_name for r in registros if r.attachment_name]

