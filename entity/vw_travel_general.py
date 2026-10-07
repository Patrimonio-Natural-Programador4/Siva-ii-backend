from sqlalchemy import Column, String, Integer, Date, Boolean, Numeric
from database.database import Base

class VwTravelGeneral(Base):
    __tablename__ = 'vw_travel_general'
    
    code = Column(String, primary_key=True)                     #codigo viaje
    traveler = Column(String)                                   #viajero
    request_date = Column(Date)                                 #fecha solicitud
    travel_start_date = Column(Date)                            #fecha inicio viaje
    travel_end_date = Column(Date)                              #fecha fin viaje
    requires_advance_payment = Column(Boolean)                  #requiere anticipo
    requested_advance_amount = Column(Numeric)                  #valor anticipo
    total_days = Column(Integer)                                #numero dias
    status = Column(String)                                     #estado
    budget_item = Column(String)                                #rubro
    expense_category = Column(String)                           #categoria
    travel_purpose = Column(String)                             #proposito
    general_additional_comments = Column(String)                #observaciones adicionales
    supervisor = Column(String)                                 #supervisor
    program = Column(String)                                    #programa
    is_international_travel = Column(Boolean)                   #es internacional
    is_guest_travel = Column(Boolean)                           #es invitado
    birth_date = Column(Date)                                   #fecha nacimiento
    mobile_phone = Column(String)                               #telefono
    emergency_contact_name = Column(String)                     #nombre contacto emergencia
    emergency_contact_phone = Column(String)                    #telefono contacto emergencia
    emergency_relationship = Column(String)                     #parentesco contacto emergencia
    includes_food = Column(Boolean)                             #incluye alimentación
