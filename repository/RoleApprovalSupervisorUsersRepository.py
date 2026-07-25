
import logging
from sqlalchemy.orm import Session
from entity.vw_role_approval_supervisor_users import VWRoleApprovalSupervisorUsers
from exceptions import PruebaNotFoundError


def listar(db: Session) -> list[VWRoleApprovalSupervisorUsers]:
    try:
        return db.query(VWRoleApprovalSupervisorUsers).order_by(VWRoleApprovalSupervisorUsers.user_name.asc()).all()
    except Exception as e:
        logging.error(f"Failed to list role approval supervisor users: {str(e)}")
        raise PruebaNotFoundError(str(e))