

# ***************************************
# 1. AgreementsRepository.py -- 22 Septiembre 2026
# ***************************************

# -----------------------------------------------------------------------------
# BLOQUE 1: Importación de Dependencias y Módulos
# -----------------------------------------------------------------------------
# Se importan las librerías necesarias para el manejo de logs, ejecución de
# consultas SQL relacionales con SQLAlchemy, definición de DTOs y excepciones.
import logging
from sqlalchemy.orm import Session
from sqlalchemy import text
from dto.AgreementsDTO import AgreementItemDTO  
from exceptions import PruebaNotFoundError  


# -----------------------------------------------------------------------------
# BLOQUE 2: Definición de la Función Principal del Repositorio
# -----------------------------------------------------------------------------
# Esta función actúa como la interfaz de acceso a datos para listar convenios.
# Recibe la sesión activa de la base de datos (db), parámetros opcionales de filtro
# y la configuración de paginación (p_page, p_page_size).
def listar_convenios_sp(
    db: Session,
    p_agreement_id: int = None,
    p_type_ids: list[int] = None,
    p_modality_ids: list[int] = None,
    p_core_ids: list[int] = None,
    p_pillar_ids: list[int] = None,
    p_years: list[int] = None,
    p_phase: list[str] = None,
    p_stage_ids: list[int] = None,
    p_priority: list[str] = None,
    p_alert: list[str] = None,
    p_search: str = None,
    p_page: int = 1,
    p_page_size: int = 25
) -> list[AgreementItemDTO]:
    try:
        # ---------------------------------------------------------------------
        # BLOQUE 3: Ejecución de la Función/Procedimiento en PostgreSQL
        # ---------------------------------------------------------------------
        # Se invoca la función nativa 'public.list_agreements' pasando los filtros 
        # mediante marcadores de posición nombrados (:p_...) para prevenir inyecciones SQL.
        result = db.execute(
            text("""
                SELECT * FROM public.list_agreements(
                    :p_agreement_id,
                    :p_type_ids,
                    :p_modality_ids,
                    :p_core_ids,
                    :p_pillar_ids,
                    :p_years,
                    :p_phase,
                    :p_stage_ids,
                    :p_priority,
                    :p_alert,
                    :p_search,
                    :p_page,
                    :p_page_size
                )
            """),
            {
                'p_agreement_id': p_agreement_id,
                'p_type_ids': p_type_ids,
                'p_modality_ids': p_modality_ids,
                'p_core_ids': p_core_ids,
                'p_pillar_ids': p_pillar_ids,
                'p_years': p_years,
                'p_phase': p_phase,
                'p_stage_ids': p_stage_ids,
                'p_priority': p_priority,
                'p_alert': p_alert,
                'p_search': p_search,
                'p_page': p_page,
                'p_page_size': p_page_size
            }
        ).fetchall()

        # ---------------------------------------------------------------------
        # BLOQUE 4: Mapeo de Tuplas SQL a Objetos DTO (Data Transfer Objects)
        # ---------------------------------------------------------------------
        # Transforma cada fila (row) devuelta por la base de datos en una instancia 
        # fuertemente tipada de AgreementItemDTO utilizando la posición de las columnas.
        convenios = [
            AgreementItemDTO(
                id=row[0],                      # Identificador único del convenio
                codigo_siva=row[1],             # Código asignado en SIVA
                nombre_convenio=row[2],         # Título/Nombre del convenio
                objeto_acuerdo=row[3],          # Descripción u objeto del acuerdo
                prioridad_acuerdo=row[4],       # Nivel de prioridad
                ano_ejecucion=row[5],           # Año de ejecución
                estado_name=row[6],             # Nombre del estado actual
                estado_stage=row[7],            # Etapa del estado
                estado_status=row[8],           # Estado operativo
                estado_color=row[9],            # Código de color HEX/CSS para la interfaz
                tipo_name=row[10],              # Tipo de convenio
                tipo_color=row[11],             # Color representativo del tipo
                modalidad_name=row[12],         # Modalidad de selección/contratación
                pilar_name=row[13],             # Pilar del programa asociado
                pilar_color=row[14],            # Color del pilar
                nucleos=row[15],                # Núcleos temáticos asociados
                implementadoras=row[16],        # Entidades implementadoras
                monto_apropiado=row[17],        # Monto presupuestado
                monto_total_apropiado=row[18],  # Monto total presupuestado acumulado
                total_paa=row[19],              # Total asignado en PAA
                total_registros=row[20]         # Conteo total para soporte de paginación
            )
            for row in result
        ]

        # Se retorna la lista de DTOs procesada
        return convenios

    # -------------------------------------------------------------------------
    # BLOQUE 5: Control de Excepciones y Registro de Errores
    # -------------------------------------------------------------------------
    # En caso de fallo en la consulta SQL o en la conexión, se registra el detalle 
    # en el log de la aplicación y se eleva la excepción de negocio 'PruebaNotFoundError'.
    except Exception as e:
        logging.error(f"Failed to fetch Acuerdos: {str(e)}")
        raise PruebaNotFoundError(str(e))