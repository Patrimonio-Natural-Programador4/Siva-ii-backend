from datetime import date, datetime, datetime

from repository import ApprovalCategoryRepository, SolicitudesAprobacionRepository
from sqlalchemy.orm import Session
from sqlalchemy import asc, func
import logging


# def obtener_anticipo_reintegro_por_tipo_y_relacion(id_tipo: int, id_relacion: int, es_reintegro: bool, db: Session) -> AnticiposReintegros:
#     try:
#         filtros = [
#             AnticiposReintegros.id_tipo_anticipo == id_tipo,
#             AnticiposReintegros.id_relacion == id_relacion,
#         ]

#         if es_reintegro is not None:
#             filtros.append(AnticiposReintegros.es_reintegro == es_reintegro)

#         anticipo = db.query(AnticiposReintegros).filter(*filtros).first()


#         # anticipo = db.query(AnticiposReintegros).filter(
#         #     AnticiposReintegros.id_tipo_anticipo == id_tipo,
#         #     AnticiposReintegros.id_relacion == id_relacion,
#         #     AnticiposReintegros.es_reintegro == False if es_reintegro is None else es_reintegro
#         # ).first()
#         return anticipo
#     except Exception as e:
#         logging.error(f"Failed to fetch anticipo: {str(e)}")
#         raise PruebaNotFoundError(str(e))
    
