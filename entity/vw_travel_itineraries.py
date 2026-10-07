from sqlalchemy import Column, String, Date, Boolean, Time
from database.database import Base

class VwTravelItinerary(Base):
    __tablename__ = 'vw_travel_itineraries'
    
    code = Column(String, primary_key=True)                     #codigo viaje
    traveler = Column(String, primary_key=True)                 #viajero
    origin_department = Column(String)                          #departamento origen
    origin_municipality = Column(String)                        #municipio origen
    destination_department = Column(String)                     #departamento destino
    destination_municipality = Column(String)                   #municipio destino
    requires_air_tickets = Column(Boolean)                      #requiere tiquetes aereos
    travel_date = Column(Date, primary_key=True)                #fecha de viaje
    estimated_departure_time = Column(Time)                     #hora estimada de salida
    is_rural_destination = Column(Boolean)                      #es destino rural
    itinerary_additional_comments = Column(String)              #observaciones adicionales
