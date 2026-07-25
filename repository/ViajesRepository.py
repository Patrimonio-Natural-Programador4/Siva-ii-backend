from sqlalchemy.orm import Session
import logging
from dto.ViajesDTO import ViajesListSP
from entity.travel_requests import TravelRequests
from exceptions import PruebaNotFoundError
from sqlalchemy import and_, or_, text

def numero_viajes(db: Session) -> int:
    try:
        return db.query(TravelRequests).count()
    except Exception as e:
        logging.error(f"Failed to fetch viajes: {str(e)}")
        raise PruebaNotFoundError(str(e))
    
def obtener_viaje_por_id(guid: str, db: Session) -> TravelRequests:
    try:
        viaje = db.query(TravelRequests).filter(TravelRequests.guid == guid).first()
        if not viaje:
            raise PruebaNotFoundError(f"Viaje with guid {guid} not found")
        return viaje
    except Exception as e:
        logging.error(f"Failed to fetch viaje with guid {guid}: {str(e)}")
        raise PruebaNotFoundError(str(e))
    

def listar_viajes_por_usuario_sp(guidmsf: str, db: Session, page: int = 1, estado: list[int] = [-1],
    filtro: str = "", fechaDesde: str = None, fechaHasta: str = None, programa: int = None) -> list[ViajesListSP]:
    try:
        programa = programa if programa is not None else -1
        print(guidmsf, page, estado, filtro, fechaDesde, fechaHasta, programa)
        result = db.execute(
            text("""
                SELECT * FROM list_travels(:guid_usuario_msft, :page, :v_status, :filtro, :fechaDesde, :fechaHasta, :programa)
            """), 
            {
                'guid_usuario_msft': guidmsf,
                'page': page,
                'v_status': estado,
                'filtro': filtro,
                'fechaDesde': fechaDesde,
                'fechaHasta': fechaHasta,
                'programa': programa
            }
        ).fetchall()


        viajes = [
            ViajesListSP(
                guid=row[0],                # Primera columna: id_viaje
                codigo=row[1],              # Segunda columna: id_viajero
                usuario=row[2],     # Tercera columna: fecha_inicio_viaje
                fecha_solicitud=row[3],        # Cuarta columna: fecha_fin_viaje
                fecha_inicio_viaje=row[4],                 # Quinta columna: codigo
                fecha_fin_viaje=row[5],    # Sexta columna: id_estado_solicitud
                requiere_anticipo=row[6],   # Séptima columna: pendien_mi_aprobacion
                estado=row[7],   # Séptima columna: pendien_mi_aprobacion
                id_estado=row[8],   # Séptima columna: id_estado
                pendiente_mi_aprobacion=row[9],   # Séptima columna: pendiente_mi_aprobacion
                id_viaje=row[10],              # Octava columna: id_viaje
                id_solicitud_aprobacion_legalizacion=row[11],
                id_solicitud_aprobacion=row[12],
                id_usuario=row[13],
                guid_usr=row[14],
                orden_actual_solicitud=row[15],
                aprobo_supervisor=row[16],
                guid_msft_ajuste=row[17],
                dias_despues_finalizado=row[18],
                legalizacion_fuera_tiempo=row[19],
                regional=row[20],
                id_regional=row[21],
                valor_anticipo=row[22],
                total_registros=row[23]
            )
            for row in result
        ]


        return viajes
    except Exception as e:
        logging.error(f"Failed to fetch viajes ")
        raise PruebaNotFoundError(str(e))
    
