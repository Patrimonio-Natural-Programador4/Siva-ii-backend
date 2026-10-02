from sqlalchemy.orm import Session
from entity.vw_travel_general import VwTravelGeneral
from entity.vw_travel_itineraries import VwTravelItinerary
from entity.vw_travel_accommodations import VwTravelAccommodation
from entity.vw_travel_legalizations import VwTravelLegalization
from entity.travel_requests import TravelRequests
from sqlalchemy import func
import logging

def get_all_general(db: Session):
    try:
        return db.query(VwTravelGeneral).join(TravelRequests, VwTravelGeneral.code == TravelRequests.code).order_by(func.coalesce(TravelRequests.request_date, TravelRequests.created_at).asc()).all()
    except Exception as e:
        logging.error(f"Failed to fetch vw_travel_general: {str(e)}")
        raise

def get_all_itineraries(db: Session):
    try:
        return db.query(VwTravelItinerary).join(TravelRequests, VwTravelItinerary.code == TravelRequests.code).order_by(func.coalesce(TravelRequests.request_date, TravelRequests.created_at).asc()).all()
    except Exception as e:
        logging.error(f"Failed to fetch vw_travel_itineraries: {str(e)}")
        raise

def get_all_accommodations(db: Session):
    try:
        return db.query(VwTravelAccommodation).join(TravelRequests, VwTravelAccommodation.code == TravelRequests.code).order_by(func.coalesce(TravelRequests.request_date, TravelRequests.created_at).asc()).all()
    except Exception as e:
        logging.error(f"Failed to fetch vw_travel_accommodations: {str(e)}")
        raise

def get_all_legalizations(db: Session):
    try:
        return db.query(VwTravelLegalization).join(TravelRequests, VwTravelLegalization.code == TravelRequests.code).order_by(func.coalesce(TravelRequests.request_date, TravelRequests.created_at).asc()).all()
    except Exception as e:
        logging.error(f"Failed to fetch vw_travel_legalizations: {str(e)}")
        raise
