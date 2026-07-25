
import logging

from sqlalchemy.orm import Session
from entity.programs import Programs
from entity.users_programs import UsersPrograms
from exceptions import PruebaNotFoundError


def listar(id_usuario: int, db: Session) -> list[UsersPrograms]:
    try:
        return db.query(UsersPrograms).filter(UsersPrograms.user_id == id_usuario).all()
    except Exception as e:
        logging.error(f"Failed to list programs: {str(e)}")
        raise PruebaNotFoundError(str(e))
    
def listar_ids_programas_por_usuario(id_user: int, db: Session) -> list[int]:
    try:
        return [
            row.program_id
            for row in (
                db.query(UsersPrograms)
                .filter(UsersPrograms.user_id == id_user)
                .order_by(UsersPrograms.program_id.asc())
                .all()
            )
        ]
    

    except Exception as e:
        logging.error(f"Failed to list user programs: {str(e)}")
        raise PruebaNotFoundError(str(e))
    
def listar_programas_por_usuario(id_user: int, db: Session) -> list[Programs]:
    try:
        return [
            row.programs
            for row in (
                db.query(UsersPrograms)
                .filter(UsersPrograms.user_id == id_user)
                .order_by(UsersPrograms.program_id.asc())
                .all()
            )
        ]
    

    except Exception as e:
        logging.error(f"Failed to list user programs: {str(e)}")
        raise PruebaNotFoundError(str(e))