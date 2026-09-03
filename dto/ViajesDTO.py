from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel
from dto.ViajesItinerarioDTO import ViajesItinerarioBase
from dto.ViajesHotelDTO import ViajesHotelBase
from dto.AnticiposReintegroDTO import AnticiposReintegrosBase
from datetime import date
import decimal

class ViajesBase(BaseModel):
    guid_usr: Optional[uuid.UUID] = None
    guid: Optional[uuid.UUID] = None
    codigo: Optional[str] = None
    id_viajero: Optional[int] = None
    objetivo_actividad: Optional[str] = None
    fecha_inicio_viaje: Optional[datetime] = None
    fecha_fin_viaje: Optional[datetime] = None
    fecha_solicitud: Optional[date] = None
    requiere_anticipo: Optional[bool] = None
    dos_o_mas_personas: Optional[bool] = None
    soporte_dos_o_mas_personas: Optional[str] = None
    numero_cuenta: Optional[str] = None
    valor_anticipo: Optional[decimal.Decimal] = None
    identificacion: Optional[int] = None
    usuario: Optional[str] = None
    estado: Optional[str] = None
    id_estado: Optional[int] = None
    id_usuario: Optional[int] = None
    es_invitado: Optional[bool] = None
    persona_invitada: Optional[str] = None
    documento_persona_invitada: Optional[str] = None
    telefono_persona_invitada: Optional[str] = None
    correo_persona_invitada: Optional[str] = None
    tipo_solicitud_aprobacion: Optional[str] = None
    tipo_viaje: Optional[str] = None
    hora_inicio: Optional[str] = None
    hora_fin: Optional[str] = None
    viaje_internacional: Optional[bool] = None
    pais: Optional[str] = None
    fecha_nacimiento_viajero: Optional[date] = None
    id_supervisor_aprueba: Optional[int] = None
    id_rol_aprobacion_supervisor: Optional[int] = None
    guid_soporte_pasaporte: Optional[str] = None
    soporte_asistencia_medica: Optional[str] = None
    soporte_pasaporte: Optional[str] = None
    ruta_soporte_asistencia_medica: Optional[str] = None
    ruta_soporte_pasaporte: Optional[str] = None
    pendiente_aprobacion_usuario_actual: Optional[bool] = None
    id_proyecto: Optional[int] = None
    id_rubro: Optional[int] = None
    proyecto_rubro: Optional[str] = None
    motivo_anulo: Optional[str] = None
    fecha_anulo: Optional[date] = None
    orden_actual_solicitud: Optional[int] = None
    aprobo_supervisor: Optional[bool] = None
    observaciones_adicionales: Optional[str] = None
    menciones_json: Optional[str] = None
    id_usuarios_mencion: Optional[list] = None
    pago_anticipo_rechazado: Optional[bool] = None
    soporte_informe: Optional[str] = None
    ruta_soporte_informe: Optional[str] = None
    relacion_facturas: Optional[bool] = None
    class Config:
        from_attributes = True

class ViajesCreate(BaseModel):
    id_viaje: Optional[int] = None
    guid: Optional[uuid.UUID] = None
    codigo: Optional[str] = None
    objetivo: Optional[str] = None
    fecha_solicitud: Optional[date] = None
    requiere_anticipo: Optional[bool] = None
    dos_o_mas_personas: Optional[bool] = None
    soporte_dos_o_mas_personas: Optional[str] = None
    nombre_archivo_dos_o_mas_personas: Optional[str] = None
    itinerario: Optional[list[ViajesItinerarioBase]] = None
    hotel: Optional[list[ViajesHotelBase]] = None
    # anticipo: Optional[list[AnticiposBase]] = None
    anticipo: Optional[AnticiposReintegrosBase] = None
    reintegro: Optional[AnticiposReintegrosBase] = None
    numero_cuenta: Optional[str] = None
    id_tipo_cuenta: Optional[int] = None
    id_entidad_bancaria: Optional[int] = None
    asociado_taller: Optional[bool] = None
    id_taller: Optional[int] = None
    fecha_inicio_viaje: Optional[date] = None
    fecha_fin_viaje: Optional[date] = None
    fecha_solicitud: Optional[date] = None
    usuario: Optional[str] = None
    id_categoria: Optional[int] = None
    nro_horas: Optional[decimal.Decimal] = None
    nro_dias: Optional[decimal.Decimal] = None
    categoria: Optional[str] = None
    tipo_cuenta: Optional[str] = None
    entidad_bancaria: Optional[str] = None
    taller: Optional[str] = None
    identificacion: Optional[int] = None
    enviar_aprobacion: Optional[bool] = None
    id_solicitud_aprobacion: Optional[int] = None
    es_invitado: Optional[bool] = None
    persona_invitada: Optional[str] = None
    documento_persona_invitada: Optional[str] = None
    telefono_persona_invitada: Optional[str] = None
    correo_persona_invitada: Optional[str] = None
    informe_lugar: Optional[str] = None
    instituciones_participantes: Optional[str] = None
    temas_tratados: Optional[str] = None
    compromisos: Optional[str] = None
    observaciones_informe: Optional[str] = None
    id_solicitud_aprobacion_legalizacion: Optional[int] = None
    fecha_inicio_taller: Optional[date] = None
    fecha_fin_taller: Optional[date] = None
    requiere_tiquetes: Optional[bool] = None
    tipo_viaje: Optional[str] = None
    hora_inicio: Optional[str] = None
    hora_fin: Optional[str] = None
    viaje_internacional: Optional[bool] = None
    pais: Optional[str] = None
    fecha_nacimiento_viajero: Optional[date] = None
    guid_msft: Optional[uuid.UUID] = None
    id_estado: Optional[int] = None
    id_supervisor_aprueba: Optional[int] = None
    id_rol_aprobacion_supervisor: Optional[int] = None
    guid_soporte_pasaporte: Optional[str] = None
    soporte_asistencia_medica: Optional[str] = None
    soporte_pasaporte: Optional[str] = None
    ruta_soporte_asistencia_medica: Optional[str] = None
    ruta_soporte_pasaporte: Optional[str] = None
    pendiente_aprobacion_usuario_actual: Optional[bool] = None
    id_proyecto: Optional[int] = None
    id_rubro: Optional[int] = None
    proyecto_rubro: Optional[str] = None
    estado: Optional[str] = None
    motivo_anulo: Optional[str] = None
    fecha_anulo: Optional[date] = None
    orden_actual_solicitud: Optional[int] = None
    aprobo_supervisor: Optional[bool] = None
    observaciones_adicionales: Optional[str] = None
    menciones_json: Optional[str] = None
    id_usuarios_mencion: Optional[list] = None
    pago_anticipo_rechazado: Optional[bool] = None
    soporte_informe: Optional[str] = None
    ruta_soporte_informe: Optional[str] = None
    relacion_facturas: Optional[bool] = None
    id_actividad: Optional[int] = None
    contacto_emergencia: Optional[str] = None
    telefono_emergencia: Optional[str] = None
    parentesco_emergencia: Optional[str] = None
    id_programa: Optional[int] = None
    valor_anticipo: Optional[decimal.Decimal] = None
    rubro_corto: Optional[str] = None
    rubro: Optional[str] = None
    actividad: Optional[str] = None
    anio_rubro: Optional[int] = None
    id_rubro: Optional[int] = None
    class Config:
        from_attributes = True



class ViajesListSP(BaseModel):
    guid: Optional[uuid.UUID] = None
    codigo: Optional[str] = None
    usuario: Optional[str] = None
    fecha_solicitud: Optional[date] = None
    fecha_inicio_viaje: Optional[datetime] = None
    fecha_fin_viaje: Optional[datetime] = None
    requiere_anticipo: Optional[bool] = None
    dos_o_mas_personas: Optional[bool] = None
    valor_anticipo: Optional[decimal.Decimal] = None
    estado: Optional[str] = None
    id_estado: Optional[int] = None
    pendiente_mi_aprobacion: Optional[bool] = None
    id_viaje: Optional[int] = None
    id_usuario: Optional[int] = None
    id_solicitud_aprobacion_legalizacion: Optional[int] = None
    id_solicitud_aprobacion: Optional[int] = None
    tipo_solicitud_aprobacion: Optional[str] = None
    guid_usr: Optional[uuid.UUID] = None
    orden_actual_solicitud: Optional[int] = None
    valor_reintegro: Optional[decimal.Decimal] = None
    aprobo_supervisor: Optional[bool] = None
    guid_msft_ajuste: Optional[uuid.UUID] = None
    pago_anticipo_rechazado: Optional[bool] = None
    dias_despues_finalizado: Optional[int] = None
    legalizacion_fuera_tiempo: Optional[str] = None
    id_regional: Optional[int] = None
    regional: Optional[str] = None
    total_registros: Optional[int] = None
    
    class Config:
        from_attributes = True

class ViajesCalendar(BaseModel):
    id: Optional[uuid.UUID] = None
    title: Optional[str] = None
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    class Config:
        from_attributes = True