from sqlalchemy import Column, String, Date, Numeric
from database.database import Base

class VwTravelLegalization(Base):
    __tablename__ = 'vw_travel_legalizations'
    
    code = Column(String, primary_key=True)                     #codigo viaje
    traveler = Column(String, primary_key=True)                 #viajero
    legalization_date = Column(Date)                            #fecha legalización
    transaction_number = Column(String, primary_key=True)       #numero transacción
    legalization_beneficiary = Column(String)                   #beneficiario legalización
    beneficiary_nit = Column(String)                            #nit beneficiario
    regimen_type = Column(String)                               #tipo de regimen
    legalized_subtotal = Column(Numeric)                        #subtotal legalizado
    legalized_iva = Column(Numeric)                             #iva legalizado
    retention_percentage = Column(Numeric)                      #porcentaje retención
    retention = Column(Numeric)                                 #retención
    total_paid = Column(Numeric)                                #total pagado
    outlay_observations = Column(String)                        #observaciones de desembolso
    legalization_observations = Column(String)                  #observaciones de legalización
