from typing import Optional
from pydantic import BaseModel
from dto.AnticiposDetalleDTO import AnticiposDetalleBase
import decimal


class AnticiposReintegrosBase(BaseModel):
    id_anticipo: Optional[int] = None
    id_relacion: Optional[int] = None
    id_tipo_anticipo: Optional[int] = None
    codigo: Optional[str] = None
    soporte_pago: Optional[str] = None
    estado: Optional[str] = None
    detalle: Optional[list[AnticiposDetalleBase]] = None
    valor: Optional[decimal.Decimal] = None
    nombre_tercero: Optional[str] = None
    numero_cuenta: Optional[str] = None
    id_entidad_bancaria: Optional[int] = None
    ruta_soporte_pago: Optional[str] = None
    soporte_pago: Optional[str] = None
    es_reintegro: Optional[bool] = None
    codigo_instrumento: Optional[bool] = None
    id_tipo_cuenta: Optional[int] = None
    codigo_instrumento: Optional[str] = None
    numero_retiros: Optional[int] = None
    gastos_bancarios: Optional[decimal.Decimal] = None
    rpc: Optional[str] = None
    ruta_rpc: Optional[str] = None
    documento_contable: Optional[str] = None
    ruta_documento_contable: Optional[str] = None
    id_estado: Optional[int] = None
    documento_consignacion_bancaria: Optional[str] = None
    ruta_documento_consignacion_bancaria: Optional[str] = None
    comprobante_egreso: Optional[str] = None
    ruta_comprobante_egreso: Optional[str] = None
    guid_relacion: Optional[str] = None
    pago_rechazado: Optional[bool] = None
    documento_legalizacion: Optional[str] = None
    ruta_documento_legalizacion: Optional[str] = None
    diminucion_rpc: Optional[str] = None
    ruta_diminucion_rpc: Optional[str] = None
    documento_soporte: Optional[str] = None
    ruta_documento_soporte: Optional[str] = None
    class Config:
        from_attributes = True