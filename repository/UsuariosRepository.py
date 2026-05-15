import logging
from sqlalchemy import text
from sqlalchemy.orm import Session
from entity.users import Users
from exceptions import PruebaNotFoundError

def listar(db: Session) -> list[Users]:
    try:
        usuarios = db.query(Users).order_by(
            Users.guid_msft.is_(None).desc(),
            Users.first_name.asc()
        ).all()
        return usuarios
    except Exception as e:
        logging.error(f"Failed to list users: {str(e)}")
        raise PruebaNotFoundError(str(e))
    
def obtener_por_guid(guid: str, db: Session) -> Users:
    try:
        usuario = db.query(Users).filter(Users.guid == guid).first()
        if not usuario:
            raise PruebaNotFoundError(f"Usuario with guid {guid} not found")
        return usuario
    except Exception as e:
        logging.error(f"Failed to get user by guid: {str(e)}")
        raise PruebaNotFoundError(str(e))


def listar_programas_por_usuario(id_user: int, db: Session) -> list[int]:
    try:
        result = db.execute(
            text("SELECT id_program FROM users_programs WHERE id_user = :id_user ORDER BY id_program"),
            {"id_user": id_user},
        )
        return [int(row[0]) for row in result.fetchall()]
    except Exception as e:
        logging.error(f"Failed to list user programs: {str(e)}")
        raise PruebaNotFoundError(str(e))


def listar_roles_por_usuario(id_user: int, db: Session) -> list[int]:
    try:
        result = db.execute(
            text("SELECT role_id FROM model_has_roles WHERE model_id = :id_user ORDER BY role_id"),
            {"id_user": id_user},
        )
        return [int(row[0]) for row in result.fetchall()]
    except Exception as e:
        logging.error(f"Failed to list user roles: {str(e)}")
        raise PruebaNotFoundError(str(e))


def obtener_model_type_por_usuario(id_user: int, db: Session) -> str:
    try:
        by_user = db.execute(
            text("SELECT model_type FROM model_has_roles WHERE model_id = :id_user LIMIT 1"),
            {"id_user": id_user},
        ).first()
        if by_user and by_user[0]:
            return str(by_user[0])

        any_row = db.execute(text("SELECT model_type FROM model_has_roles LIMIT 1")).first()
        if any_row and any_row[0]:
            return str(any_row[0])

        return 'App\\\\Models\\\\User'
    except Exception as e:
        logging.error(f"Failed to infer model_type for user roles: {str(e)}")
        return 'App\\\\Models\\\\User'


def reemplazar_programas_usuario(id_user: int, program_ids: list[int], db: Session) -> None:
    try:
        db.execute(text("DELETE FROM users_programs WHERE id_user = :id_user"), {"id_user": id_user})

        for id_program in sorted(set(int(x) for x in program_ids)):
            db.execute(
                text("INSERT INTO users_programs (id_user, id_program) VALUES (:id_user, :id_program)"),
                {"id_user": id_user, "id_program": id_program},
            )
    except Exception as e:
        logging.error(f"Failed to replace user programs: {str(e)}")
        raise PruebaNotFoundError(str(e))


def reemplazar_roles_usuario(id_user: int, role_ids: list[int], model_type: str, db: Session) -> None:
    try:
        db.execute(text("DELETE FROM model_has_roles WHERE model_id = :id_user"), {"id_user": id_user})

        for role_id in sorted(set(int(x) for x in role_ids)):
            db.execute(
                text(
                    "INSERT INTO model_has_roles (role_id, model_type, model_id) "
                    "VALUES (:role_id, :model_type, :model_id)"
                ),
                {"role_id": role_id, "model_type": model_type, "model_id": id_user},
            )
    except Exception as e:
        logging.error(f"Failed to replace user roles: {str(e)}")
        raise PruebaNotFoundError(str(e))


def guardar(db: Session) -> None:
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to commit user transaction: {str(e)}")
        raise PruebaNotFoundError(str(e))