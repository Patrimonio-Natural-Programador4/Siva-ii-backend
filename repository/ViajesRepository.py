from sqlalchemy.orm import Session, joinedload
from entity.travel_legalizations import TravelLegalizations
import logging
from datetime import datetime, time
from decimal import Decimal
from dto.ViajesDTO import ViajesCalendar, ViajesListSP, TravelLegalizationCreate
from entity.travel_requests import TravelRequests
from entity.travel_advances import TravelAdvances
from entity.users import Users
from exceptions import PruebaNotFoundError
from sqlalchemy import and_, func, or_, text

def numero_viajes(db: Session) -> int:
    try:
        return db.query(TravelRequests).count()
    except Exception as e:
        logging.error(f"Failed to fetch viajes: {str(e)}")
        raise PruebaNotFoundError(str(e))
    
def obtener_por_guid(guid: str, db: Session) -> TravelRequests:
    try:
        viaje = db.query(TravelRequests).filter(TravelRequests.guid == guid).first()
        if not viaje:
            raise PruebaNotFoundError(f"Viaje with guid {guid} not found")
        return viaje
    except Exception as e:
        logging.error(f"Failed to fetch viaje with guid {guid}: {str(e)}")
        raise PruebaNotFoundError(str(e))

def obtener_por_guid_id_solicitud_aprobacion(guid: str, id_solicitud_aprobacion, db: Session) -> TravelRequests:
    try:
        viaje = db.query(TravelRequests).filter(
                    or_(
                        and_(
                            TravelRequests.approval_request_id == id_solicitud_aprobacion,
                            TravelRequests.guid == guid
                        ),
                        and_(
                            TravelRequests.expense_approval_request_id == id_solicitud_aprobacion,
                            TravelRequests.guid == guid
                        )
                    )
                ).first()
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


def listar_viajes_calendario(db: Session, fecha_desde, fecha_hasta) -> list[ViajesCalendar]:
    try:
        fecha_fin_viaje = func.coalesce(TravelRequests.travel_end_date, TravelRequests.travel_start_date)
        result = db.query(TravelRequests, Users.full_name).join(
            Users,
            TravelRequests.traveler_user_id == Users.id
        ).filter(
            TravelRequests.travel_start_date.isnot(None),
            TravelRequests.travel_start_date < fecha_hasta,
            fecha_fin_viaje >= fecha_desde,
            or_(TravelRequests.is_cancelled.is_(None), TravelRequests.is_cancelled.is_(False))
        ).order_by(
            TravelRequests.travel_start_date.asc(),
            TravelRequests.code.asc()
        ).all()

        return [
            ViajesCalendar(
                id=viaje.guid,
                title=f"{viaje.code or ''} - {usuario or ''}".strip(" -"),
                start=datetime.combine(viaje.travel_start_date, time.min),
                end=datetime.combine(viaje.travel_end_date or viaje.travel_start_date, time.min)
            )
            for viaje, usuario in result
        ]
    except Exception as e:
        logging.error(f"Failed to fetch viajes calendar: {str(e)}")
        raise PruebaNotFoundError(str(e))
    
def crear_factura(db: Session, legalizacion: TravelLegalizationCreate) -> TravelLegalizations:
    try:
        nuevo_registro = TravelLegalizations(**legalizacion.dict())
        db.add(nuevo_registro)
        db.commit()
        db.refresh(nuevo_registro)
        return nuevo_registro
    except Exception as e:
        db.rollback()
        logging.error(f"Error al crear factura: {str(e)}")
        raise e

def obtener_legalizaciones_por_viaje(db: Session, travel_request_id: int) -> list[TravelLegalizations]:
    return (
        db.query(TravelLegalizations)
        .options(
            joinedload(TravelLegalizations.regimen_type),
            joinedload(TravelLegalizations.concept),
        )
        .filter(TravelLegalizations.travel_request_id == travel_request_id)
        .order_by(TravelLegalizations.legalization_id.asc())
        .all()
    )

def obtener_legalizacion_por_viaje(db: Session, travel_request_id: int) -> TravelLegalizations:
    return (
        db.query(TravelLegalizations)
        .options(joinedload(TravelLegalizations.regimen_type))
        .filter(TravelLegalizations.travel_request_id == travel_request_id)
        .first()
    )

def obtener_legalizacion_por_id(db: Session, legalization_id: int) -> TravelLegalizations:
    return (
        db.query(TravelLegalizations)
        .options(joinedload(TravelLegalizations.regimen_type))
        .filter(TravelLegalizations.legalization_id == legalization_id)
        .first()
    )

def actualizar_legalizacion(db: Session, legalization_id: int, datos_actualizar: dict) -> TravelLegalizations:
    try:
        legalizacion = (
            db.query(TravelLegalizations)
            .options(joinedload(TravelLegalizations.regimen_type))
            .filter(TravelLegalizations.legalization_id == legalization_id)
            .first()
        )
        if not legalizacion:
            return None

        for key, value in datos_actualizar.items():
            if hasattr(legalizacion, key) and key != 'legalization_id':
                setattr(legalizacion, key, value)

        db.commit()
        db.refresh(legalizacion)
        db.expire(legalizacion, ['regimen_type'])
        return legalizacion
    except Exception as e:
        db.rollback()
        logging.error(f"Error al actualizar legalizacion: {str(e)}")
        raise e


def listar_anticipos_por_viaje(travel_request_id: int, db: Session) -> list[TravelAdvances]:
    return (
        db.query(TravelAdvances)
        .options(joinedload(TravelAdvances.concept))
        .filter(TravelAdvances.travel_request_id == travel_request_id)
        .order_by(TravelAdvances.travel_advance_id.asc())
        .all()
    )


def actualizar_anticipos_viaje(
    travel_request_id: int,
    anticipos: list,
    total: Decimal,
    db: Session,
) -> None:
    try:
        existentes = db.query(TravelAdvances).filter(
            TravelAdvances.travel_request_id == travel_request_id
        ).all()
        existentes_por_id = {item.travel_advance_id: item for item in existentes}
        ids_conservados = set()

        for item in anticipos:
            advance_id = item.travel_advance_id
            registro = existentes_por_id.get(advance_id) if advance_id is not None else None
            if registro is None:
                registro = TravelAdvances(travel_request_id=travel_request_id)
                db.add(registro)
            else:
                ids_conservados.add(registro.travel_advance_id)

            registro.expense_advance_concept_id = item.expense_advance_concept_id
            registro.amount = item.amount or 0
            registro.observations = item.observations

        for registro in existentes:
            if registro.travel_advance_id not in ids_conservados:
                db.delete(registro)

        viaje = db.query(TravelRequests).filter(
            TravelRequests.travel_request_id == travel_request_id
        ).first()
        if viaje:
            viaje.advance_amount = total

        db.commit()
    except Exception as e:
        db.rollback()
        logging.error(f"Error al actualizar anticipos del viaje {travel_request_id}: {str(e)}")
        raise e
