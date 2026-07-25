
from sqlalchemy import Column, Integer, String, Text, Boolean

from database.database import Base


class VWRoleApprovalSupervisorUsers(Base):
    __tablename__ = 'vw_role_approval_supervisor_users'

    approval_role_id = Column(Integer)
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String)

    __mapper_args__ = {
        'primary_key': [user_id]  # Usar la columna artificial como clave primaria
    }

    @classmethod
    def __declare_last__(cls):
        pass  # Este método podría usarse para evitar operaciones de escritura adicionales