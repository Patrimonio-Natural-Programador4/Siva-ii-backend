from sqlalchemy import ARRAY, Column, DateTime, Integer, String, Date, Boolean, Uuid, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class VWApprovalRequestHistory(Base):
    __tablename__ = 'vw_approval_request_history'

    # Definición de columnas
    history_id = Column(Integer, primary_key=True)
    approval_request_id = Column(Integer, primary_key=True)
    related_record_id = Column(Integer)
    approval_workflow_id = Column(Integer)
    category_id = Column(Integer)
    approval_status_id = Column(Integer)
    approval_role_id = Column(Integer)
    user_id = Column(Integer)
    approval_status_step_id = Column(Integer)
    approved_at = Column(DateTime)
    created_at = Column(DateTime)
    comments = Column(Text)
    step_id = Column(Integer)
    step_order = Column(Integer)
    # asigna_presupuesto_viajes = Column(Boolean)
    # ajusta_itinerario_viajes = Column(Boolean)
    rol = Column(Text)
    user = Column(Text)
    approval_category = Column(Text)
    guid = Column(Uuid)
    approval_route_status = Column(Text)
    # deshabilita_conceptos_anticipo = Column(Boolean)
    # valida_soportes_hotel = Column(Boolean)
    # agrega_rpc = Column(Boolean)
    # agrega_documento_contable = Column(Boolean)
    is_supervisor = Column(Boolean)
    # ids_usuarios_delegados = Column(ARRAY(Integer()))
    # habilitar_pago = Column(Boolean)
    # habilitar_rechazar_pago = Column(Boolean)
    __mapper_args__ = {
        'primary_key': [history_id]
    }
    @classmethod
    def __declare_last__(cls):
        """ Evitar que se pueda hacer commit en esta clase (solo lectura). """
        pass

