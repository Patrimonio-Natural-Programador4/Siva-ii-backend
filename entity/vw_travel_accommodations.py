from sqlalchemy import Column, String, Date
from database.database import Base

class VwTravelAccommodation(Base):
    __tablename__ = 'vw_travel_accommodations'
    
    code = Column(String, primary_key=True)                     #codigo viaje
    traveler = Column(String, primary_key=True)                 #viajero
    accommodation_department = Column(String)                   #departamento alojamiento
    accommodation_municipality = Column(String)                 #municipio alojamiento
    check_in_date = Column(Date, primary_key=True)              #fecha check in
    check_out_date = Column(Date)                               #fecha check out
    accommodation_additional_comments = Column(String)          #observaciones adicionales
