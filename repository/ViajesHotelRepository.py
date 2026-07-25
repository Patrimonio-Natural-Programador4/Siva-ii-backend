import logging
from sqlalchemy.orm import Session
from entity.travel_accommodations import TravelAccommodations
from exceptions import PruebaNotFoundError

def obtener_hotel_por_id(id_viaje_hotel: int, id_viaje: int, db: Session) -> TravelAccommodations:
    try:
        hotel = db.query(TravelAccommodations).filter(TravelAccommodations.travel_request_id == id_viaje, TravelAccommodations.travel_accommodation_id == id_viaje_hotel).first()
        return hotel
    except Exception as e:
        logging.error(f"Failed to fetch hotel: {str(e)}")
        raise PruebaNotFoundError(str(e))

def listar_hoteles_por_viaje(id_viaje: int, db: Session) -> list[TravelAccommodations]:
    try:
        hoteles = db.query(TravelAccommodations).filter(TravelAccommodations.travel_request_id == id_viaje).all()
        return hoteles
    except Exception as e:
        logging.error(f"Failed to fetch hoteles for viaje {id_viaje}: {str(e)}")
        raise PruebaNotFoundError(str(e))