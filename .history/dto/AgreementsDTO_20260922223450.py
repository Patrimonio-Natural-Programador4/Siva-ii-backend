# ***************************************
# 1. AgreementsDTO.py -- 22 Septiembre 2026
# ***************************************

# -----------------------------------------------------------------------------
# BLOQUE 1: Importación de Librerías y Tipos
# -----------------------------------------------------------------------------
# Se importan los tipos nativos de Python para manejo de fechas, decimales y 
# valores opcionales, además de 'BaseModel' de Pydantic para la definición 
# y validación de esquemas de datos.
import decimal
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


# -----------------------------------------------------------------------------
# BLOQUE 2: DTO Base de Convenios (AgreementsBase)
# -----------------------------------------------------------------------------
# Define los atributos principales e información general de un convenio.
# Se utiliza como clase padre o estructura estándar de transferencia para 
# datos generales de la entidad.
class AgreementsBase(BaseModel):
    id: Optional[int] = None                                # ID único del convenio en BD
    codigo_siva: Optional[str] = None                       # Código institucional (ej. C-2026-1)
    nombre_convenio: Optional[str] = None                   # Nombre o título descriptivo del convenio
    objeto_acuerdo: Optional[str] = None                    # Objeto o finalidad del convenio
    prioridad_acuerdo: Optional[str] = None                 # Prioridad asignada (Alta, Media, Baja)
    ano_ejecucion: Optional[int] = None                     # Año fiscal o de ejecución
    monto_apropiado: Optional[decimal.Decimal] = None        # Valor presupuestal apropiado
    monto_total_apropiado: Optional[decimal.Decimal] = None  # Valor total acumulado de apropiación
    total_paa: Optional[decimal.Decimal] = None             # Total registrado en el PAA

    class Config:
        # Permite mapear directamente desde instancias de modelos ORM (SQLAlchemy)
        from_attributes = True


# -----------------------------------------------------------------------------
# BLOQUE 3: DTO de Filtros de Búsqueda (AgreementsFilterDTO)
# -----------------------------------------------------------------------------
# Encapsula todos los parámetros requeridos para filtrar y paginar el listado 
# de convenios desde los endpoints de consulta hacia los repositorios.
class AgreementsFilterDTO(BaseModel):
    p_agreement_id: Optional[int] = None            # Filtro por ID específico de convenio
    p_type_ids: Optional[list[int]] = None          # Lista de IDs para filtrar por tipos de convenio
    p_modality_ids: Optional[list[int]] = None      # Lista de IDs para filtrar por modalidad
    p_core_ids: Optional[list[int]] = None          # Lista de IDs para filtrar por núcleo
    p_pillar_ids: Optional[list[int]] = None        # Lista de IDs para filtrar por pilar
    p_years: Optional[list[int]] = None             # Lista de años para filtrado temporal
    p_phase: Optional[list[str]] = None             # Filtro por fases del convenio
    p_stage_ids: Optional[list[int]] = None         # Filtro por etapas asociadas
    p_priority: Optional[list[str]] = None          # Filtro por niveles de prioridad
    p_alert: Optional[list[str]] = None             # Filtro por estados de alerta
    p_search: Optional[str] = None                  # Búsqueda por coincidencia de texto (búsqueda libre)
    p_page: Optional[int] = 1                       # Número de página para la paginación (default: 1)
    p_page_size: Optional[int] = 25                 # Cantidad de registros por página (default: 25)

    class Config:
        from_attributes = True


# -----------------------------------------------------------------------------
# BLOQUE 4: DTO de Respuesta de Procedimiento Almacenado (AgreementsListSP)
# -----------------------------------------------------------------------------
# Representa el esquema de salida extendido retornado al ejecutar el procedimiento 
# o función almacenada 'public.list_agreements'. Incluye etiquetas formateadas 
# y colores de estado para su renderizado en la interfaz de usuario (Frontend).
class AgreementsListSP(BaseModel):
    id: Optional[int] = None                                # Identificador del convenio
    codigo_siva: Optional[str] = None                       # Código único SIVA
    nombre_convenio: Optional[str] = None                   # Nombre del convenio
    objeto_acuerdo: Optional[str] = None                    # Objeto o finalidad
    prioridad_acuerdo: Optional[str] = None                 # Nivel de prioridad
    ano_ejecucion: Optional[int] = None                     # Año de ejecución
    estado_name: Optional[str] = None                       # Nombre legible del estado actual
    estado_stage: Optional[str] = None                      # Etapa del estado actual
    estado_status: Optional[str] = None                     # Estado del flujo operativo
    estado_color: Optional[str] = None                      # Código de color HEX/CSS para el estado
    tipo_name: Optional[str] = None                         # Nombre del tipo de convenio
    tipo_color: Optional[str] = None                        # Código de color para el tipo
    modalidad_name: Optional[str] = None                    # Nombre de la modalidad
    pilar_name: Optional[str] = None                        # Nombre del pilar del programa
    pilar_color: Optional[str] = None                       # Color asignado al pilar
    nucleos: Optional[str] = None                           # Núcleos concatenados o en formato texto
    implementadoras: Optional[str] = None                   # Entidades implementadoras asociadas
    monto_apropiado: Optional[decimal.Decimal] = None       # Monto apropiado asignado
    monto_total_apropiado: Optional[decimal.Decimal] = None # Monto total presupuestado acumulado
    total_paa: Optional[decimal.Decimal] = None             # Total PAA asignado
    total_registros: Optional[int] = None                   # Cantidad total de registros (para paginador)

    class Config:
        from_attributes = True