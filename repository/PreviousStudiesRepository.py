#REPOSITORY ESTUDIOS PREVIOS

import logging
from sqlalchemy.orm import Session
from dto.PreviousStudiesDTO import PreviousStudiesListDTO
from entity.previous_studies import PreviousStudies
from exceptions import PruebaCreationError, PruebaNotFoundError
from sqlalchemy import func, select
from sqlalchemy import text, bindparam, Integer
from sqlalchemy.dialects.postgresql import ARRAY


def listar(db: Session) -> list[PreviousStudies]:
    try:
        return db.query(PreviousStudies).order_by(PreviousStudies.id.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list PreviousStudies: {str(e)}")
        raise PruebaNotFoundError(str(e))


def crear_estudio_previo(studies: PreviousStudies, db: Session) -> PreviousStudies:
    try:
        db.add(studies)
        db.commit()
        db.refresh(studies)
        return studies
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create PreviousStudies: {str(e)}")
        raise PruebaCreationError(str(e))


def obtener_por_id(id: int, db: Session) -> PreviousStudies | None:
    try:
        return db.query(PreviousStudies).filter(PreviousStudies.id == id).first()
    except Exception as e:
        logging.error(f"Failed to get PreviousStudies by id: {str(e)}")
        raise PruebaNotFoundError(str(e))
    
def obtener_por_nombre(nombre: str, db: Session) -> PreviousStudies | None:
    try:
        return db.query(PreviousStudies).filter(PreviousStudies.name.ilike(nombre.strip())).first()
    except Exception as e:
        logging.error(f"Failed to get program by name: {str(e)}")
        raise PruebaNotFoundError(str(e))
    
    
def numero_estudios_previos(db: Session) -> int:
    try:
        return db.scalar(select(func.count(PreviousStudies.id))) or 0
    except Exception as e:
        logging.error(f"Error al contar estudios previos: {str(e)}")
        raise Exception(f"Error de base de datos al contar estudios previos: {str(e)}") from e
    
    
def obtener_por_guid(guid: str, db: Session) -> PreviousStudies | None:
    try:
        return db.query(PreviousStudies).filter(PreviousStudies.guid == guid).first()
    except Exception as e:
        logging.error(f"Failed to get PreviousStudies by guid: {str(e)}")
        raise PruebaNotFoundError(str(e))
    
def obtener_por_guid_id_solicitud_aprobacion(guid: str, id_solicitud_aprobacion: int, db: Session) -> PreviousStudies | None:
    try:
        return db.query(PreviousStudies).filter(
            PreviousStudies.guid == guid,
            PreviousStudies.approval_request_id == id_solicitud_aprobacion
        ).first()
    except Exception as e:
        logging.error(f"Failed to get PreviousStudies by guid and approval_request_id: {str(e)}")
        raise PruebaNotFoundError(str(e))



def listar_previous_studies_por_usuario_sp(
    guid_usuario_msft: str,
    db: Session,
    page: int = 1,
    estado: list[int] = [-1],
    filtro: str = "",
    programa: int = -1,
) -> list[PreviousStudiesListDTO]:
    try:
        query = text("""
            SELECT sp.*, p.first_name, p.other_name, p.last_name, p.other_last_name
            FROM list_previous_studies(
                :guid_usuario_msft, :page, :v_status, :filtro, :v_program
            ) sp
            LEFT JOIN persons p ON p.id = sp.persons_id
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
            PreviousStudiesListDTO(
                precedents=row[0],
                justification=row[1],
                scope=row[2],
                overall_objective=row[3],
                term=row[4],
                obligations=row[5],
                supervisor=row[6],
                total_value=row[7],
                contributions_ei=row[8],
                total_value_executes_fpn=row[9],
                total_value_executes_ei=row[10],
                previous_studies_states_id=row[11],
                implementer_id=row[12],
                implementer=row[13],
                persons_id=row[14],
                persons_email=row[15],
                capacity_assessment_id=row[16],
                capacity_assessment=row[17],
                guid=row[18],
                program_id=row[19],
                program_name=row[20],
                contributions_fpn=row[21],
                estimated_term=row[22],
                code=row[23],
                pending_my_approval=row[24],
                approval_request_id=row[25],
                user_id=row[26],
                guid_msft=row[27],
                step_order_actual_request=row[28],
                guid_msft_adjustment=row[29],
                total_records=row[30],
                persons=" ".join(
                    part.strip() for part in [row[31], row[32] or '', row[33], row[34] or '']
                    if part and part.strip()
                ),
            )
            for row in result
        ]
    except Exception as e:
        logging.error(f"Failed to fetch previous studies: {str(e)}")
        raise PruebaNotFoundError(str(e))