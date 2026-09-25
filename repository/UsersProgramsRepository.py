
import logging

from sqlalchemy.orm import Session
from dto.ResponseRequest import ResponseRequest
from entity.programs import Programs
from entity.users_programs import UsersPrograms
from exceptions import PruebaNotFoundError
from repository import UsuariosRepository


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
    
    
    
def programas_por_usuario(id_user: int, db: Session) -> list[dict]:
    try:
        # Hacemos join con la tabla Programs
        rows = (
            db.query(UsersPrograms.program_id, Programs.name)
            .join(Programs, UsersPrograms.program_id == Programs.id)
            .filter(UsersPrograms.user_id == id_user)
            .order_by(UsersPrograms.program_id.asc())
            .all()
        )

        # Devolvemos lista de diccionarios con id y nombre
        return [
            {"program_id": row.program_id, "program_name": row.name}
            for row in rows
        ]

    except Exception as e:
        logging.error(f"Failed to list user programs: {str(e)}")
        raise PruebaNotFoundError(str(e))

 
def listado_programas_por_usuario(id_user: int, db: Session) -> list[dict]:
    try:
        # Hacemos join con la tabla Programs
        rows = (
            db.query(UsersPrograms.program_id, Programs.name)
            .join(Programs, UsersPrograms.program_id == Programs.id)
            .filter(UsersPrograms.user_id == id_user)
            .order_by(UsersPrograms.program_id.asc())
            .all()
        )

        # Devolvemos lista de diccionarios con id y nombre
        return [
            {"id_programa": row.program_id, "name": row.name}
            for row in rows
        ]

    except Exception as e:
        logging.error(f"Failed to list user programs: {str(e)}")
        raise PruebaNotFoundError(str(e))
