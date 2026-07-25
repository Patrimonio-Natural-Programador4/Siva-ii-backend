import logging
from sqlalchemy.orm import Session
from entity.travel_itineraries import TravelItineraries
from exceptions import PruebaNotFoundError


def obtener_itinerario_por_id(id_viaje_itinerario: int, id_viaje: int, db: Session) -> TravelItineraries:
    try:
        itinerario = db.query(TravelItineraries).filter(TravelItineraries.travel_request_id == id_viaje, TravelItineraries.travel_itinerary_id == id_viaje_itinerario).first()
        return itinerario
    except Exception as e:
        logging.error(f"Failed to fetch itinerario: {str(e)}")
        raise PruebaNotFoundError(str(e))
    
def listar_itinerarios_por_viaje(id_viaje: int, db: Session) -> list[TravelItineraries]:
    try:
        itinerarios = db.query(TravelItineraries).filter(TravelItineraries.travel_request_id == id_viaje).order_by(TravelItineraries.travel_date, TravelItineraries.departure_time).all()
        return itinerarios
    except Exception as e:
        logging.error(f"Failed to fetch itinerarios for viaje {id_viaje}: {str(e)}")
        raise PruebaNotFoundError(str(e))