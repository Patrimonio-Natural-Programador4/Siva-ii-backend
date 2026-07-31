import logging
from sqlalchemy import text
from sqlalchemy.orm import Session
from entity.model_has_roles import ModelHasRoles
from entity.users import Users
from entity.users_programs import UsersPrograms
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

def obtener_por_guid_msft(guid: str, db: Session) -> Users:
    try:
        usuario = db.query(Users).filter(Users.guid_msft == guid).first()
        if not usuario:
            raise PruebaNotFoundError(f"Usuario with guid {guid} not found")
        return usuario
    except Exception as e:
        logging.error(f"Failed to get user by guid: {str(e)}")
        raise PruebaNotFoundError(str(e))


def listar_roles_por_usuario(id_user: int, db: Session) -> list[int]:
    try:
        return [
            row.role_id
            for row in (
                db.query(ModelHasRoles)
                .filter(ModelHasRoles.model_id == id_user)
                .order_by(ModelHasRoles.role_id)
                .all()
            )
        ]

    except Exception as e:
        logging.error(f"Failed to list user roles: {str(e)}")
        raise PruebaNotFoundError(str(e))
    

def obtener_usuario_por_id(id_user: list[int], db: Session) -> list[Users]:
    try:
        usuarios = db.query(Users).filter(Users.id.in_(id_user)).all()
        return usuarios

    except Exception as e:
        logging.error(f"Failed to get users by id: {str(e)}")
        raise PruebaNotFoundError(str(e))



#Modulos a los que tiene acceso el usuario
def obtener_model_type_por_usuario(id_user: int, db: Session) -> str:
    try:
        row = (
            db.query(ModelHasRoles)
            .filter(ModelHasRoles.model_id == id_user)
            .first()
        )

        if row:
            return row.model_type

        row = db.query(ModelHasRoles).first()

        if row:
            return row.model_type

        return "App\\Models\\User"

    except Exception as e:
        logging.error(f"Failed to infer model_type for user roles: {str(e)}")
        return "App\\Models\\User"



def reemplazar_programas_usuario(
    id_user: int,
    program_ids: list[int],
    db: Session
) -> None:
    try:
        (
            db.query(UsersPrograms)
            .filter(UsersPrograms.user_id == id_user)
            .delete(synchronize_session=False)
        )

        db.add_all(
            [
                UsersPrograms(
                    user_id=id_user,
                    program_id=id_program,
                )
                for id_program in sorted(set(program_ids))
            ]
        )

    except Exception as e:
        logging.error(f"Failed to replace user programs: {str(e)}")
        raise PruebaNotFoundError(str(e))
 


def reemplazar_roles_usuario(
    id_user: int,
    role_ids: list[int],
    model_type: str,
    db: Session,
) -> None:
    try:
        (
            db.query(ModelHasRoles)
            .filter(ModelHasRoles.model_id == id_user)
            .delete(synchronize_session=False)
        )

        db.add_all(
            [
                ModelHasRoles(
                    role_id=role_id,
                    model_id=id_user,
                    model_type=model_type,
                )
                for role_id in sorted(set(role_ids))
            ]
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