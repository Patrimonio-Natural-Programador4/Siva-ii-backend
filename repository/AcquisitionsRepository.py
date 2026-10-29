import logging
from sqlalchemy.orm import Session
from entity.acquisitions import Acquisitions
from exceptions import PruebaCreationError, PruebaNotFoundError
from sqlalchemy import text, bindparam, Integer, Text, String
from dto.AcquisitionsDTO import AcquisitionListSP
from sqlalchemy.dialects.postgresql import ARRAY


def list_acquisitions(db: Session) -> list[Acquisitions]:
    try:
        return db.query(Acquisitions).order_by(Acquisitions.id.desc()).all()
    except Exception as e:
        logging.error(f"Failed to list Acquisitions: {str(e)}")
        raise PruebaNotFoundError(str(e))


def create_acquisition(acquisitions: Acquisitions, db: Session) -> Acquisitions:
    try:
        db.add(acquisitions)
        db.commit()
        db.refresh(acquisitions)
        return acquisitions
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to create Acquisitions: {str(e)}")
        raise PruebaCreationError(str(e))


def update_acquisition(acquisitions: Acquisitions, db: Session) -> Acquisitions:
    try:
        db.commit()
        db.refresh(acquisitions)
        return acquisitions
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to update Acquisitions: {str(e)}")
        raise PruebaCreationError(str(e))


def get_acquisition_by_id(id: int, db: Session) -> Acquisitions | None:
    try:
        return db.query(Acquisitions).filter(Acquisitions.id == id).first()
    except Exception as e:
        logging.error(f"Failed to get Acquisition by id: {str(e)}")
        raise PruebaNotFoundError(str(e))


def get_acquisition_by_process_number(process_number: int, db: Session) -> Acquisitions | bool:
    try:
        return db.query(Acquisitions).filter(Acquisitions.process_number == process_number).first()
    except Exception as e:
        logging.error(f"Failed to get Acquisitions by process_number: {str(e)}")
        return False


def has_dependencies(id: int, db: Session) -> bool:
    try:
        query = text("""
    SELECT
        EXISTS (SELECT 1 FROM acquisition_implementer WHERE acquisition_id = :id)
     OR EXISTS (SELECT 1 FROM acquisition_contract    WHERE acquisition_id = :id)
     OR EXISTS (SELECT 1 FROM notes                   WHERE acquisition_id = :id)
""")
        return bool(db.execute(query, {'id': id}).scalar())
    except Exception as e:
        logging.error(f"Failed to check Acquisitions dependencies: {str(e)}")
        raise PruebaNotFoundError(str(e))


def delete_acquisition(acquisition: Acquisitions, db: Session) -> None:
    try:
        db.delete(acquisition)
        db.commit()
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to delete Acquisitions: {str(e)}")
        raise PruebaCreationError(str(e))


def list_acquisitions_sp(
    db: Session,
    page: int = 1,
    filtro: str = "",
    pid: int = -1,
    actividad: int = -1,
    procesos: list[str] | None = None,
    rubros: list[str] | None = None,
    rubros_cortos: list[str] | None = None,
    actividad_codigo: str | None = None,                         
) -> list[AcquisitionListSP]:
    try:
        query = text("""
    SELECT sp.*
    FROM list_acquisitions(
        :page, :filter, :v_pid, :v_activity, :v_process, :v_rubros, :v_rubros_cortos, :v_activity_code
    ) sp
""").bindparams(
    bindparam('page', type_=Integer),
    bindparam('filter', type_=String),
    bindparam('v_pid', type_=Integer),
    bindparam('v_activity', type_=Integer),
    bindparam('v_process', type_=ARRAY(Text)),
    bindparam('v_rubros', type_=ARRAY(Text)),
    bindparam('v_rubros_cortos', type_=ARRAY(Text)),
    bindparam('v_activity_code', type_=Text),                    
)

        result = db.execute(
            query,
            {
                'page': page,
                'filter': (filtro or "").strip(),
                'v_pid': pid,
                'v_activity': actividad,
                'v_process': procesos or None,
                'v_rubros': rubros or None,
                'v_rubros_cortos': rubros_cortos or None,
                'v_activity_code': actividad_codigo,            
            }
        ).fetchall()

        return [
            AcquisitionListSP(**row._mapping)
            for row in result
        ]
    except Exception as e:
        logging.error(f"Failed to fetch acquisitions: {str(e)}")
        raise PruebaNotFoundError(str(e))