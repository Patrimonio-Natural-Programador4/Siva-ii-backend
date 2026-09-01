import logging
from sqlalchemy.orm import Session
from entity.capacity_assessments import CapacityAssessments
from exceptions import PruebaCreationError, PruebaNotFoundError
from sqlalchemy import text, bindparam, Integer
from dto.CapacityAssessmentsDTO import CapacityAssessmentListSP
from sqlalchemy.dialects.postgresql import ARRAY


def listar(db: Session) -> list[CapacityAssessments]:
    try:
        return db.query(CapacityAssessments).order_by(CapacityAssessments.name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list CapacityAssessments: {str(e)}")
        raise PruebaNotFoundError(str(e))


def crear(capacidad: CapacityAssessments, db: Session) -> CapacityAssessments:
    try:
        db.add(capacidad)
        db.commit()
        db.refresh(capacidad)
        return capacidad
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create CapacityAssessments: {str(e)}")
        raise PruebaCreationError(str(e))
def obtener_por_id(id: int, db: Session) -> CapacityAssessments | None:
    try:
        return db.query(CapacityAssessments).filter(CapacityAssessments.id == id).first()
    except Exception as e:
        logging.error(f"Failed to get CapacityAssessments by id: {str(e)}")
        raise PruebaNotFoundError(str(e))
    
def obtener_por_nombre(nombre: str, db: Session) -> CapacityAssessments | bool:
    try:
        return db.query(CapacityAssessments).filter(CapacityAssessments.name.ilike(nombre.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get CapacityAssessments by name: {str(e)}")
        return False
      #  raise PruebaNotFoundError(str(e))
    


def obtener_por_guid(guid: str, db: Session) -> CapacityAssessments | None:
    try:
        return db.query(CapacityAssessments).filter(CapacityAssessments.guid == guid).first()
    except Exception as e:
        logging.error(f"Failed to get CapacityAssessments by guid: {str(e)}")
        raise PruebaNotFoundError(str(e))



def listar_capacity_assessments_por_usuario_sp(
    guid_usuario_msft: str,
    db: Session,
    page: int = 1,
    estado: list[int] = [-1],
    filtro: str = "",
    programa: int = -1,
) -> list[CapacityAssessmentListSP]:
    try:
        query = text("""
            SELECT * FROM list_capacity_assesstment(
                :guid_usuario_msft, :page, :v_status, :filtro, :v_program
            )
        """).bindparams(
            bindparam('v_status', type_=ARRAY(Integer))
        )

        result = db.execute(
            query,
            {
                'guid_usuario_msft': guid_usuario_msft,
                'page': page,
                'v_status': estado,
                'filtro': filtro,
                'v_program': programa,
            }
        ).fetchall()

        return [
            CapacityAssessmentListSP(
                guid=row[0],
                codigo=row[1],
                name=row[2],
                implementer_id=row[3],
                implementer_name=row[4],
                pending_my_approval=row[5],
                capacity_assessments_id=row[6],
                approval_request_id=row[7],
                user_id=row[8],
                guid_msft=row[9],
                step_order_actual_request=row[10],
                guid_msft_adjustment=row[11],
                total_records=row[12],
            )
            for row in result
        ]
    except Exception as e:
        logging.error(f"Failed to fetch capacity assessments: {str(e)}")
        raise PruebaNotFoundError(str(e))
