"""Creación vista menu

Revision ID: 818443d98595
Revises: 1eca66bbaada
Create Date: 2026-09-11 03:53:43.613003

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '818443d98595'
down_revision: Union[str, Sequence[str], None] = '1eca66bbaada'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.execute("""
        CREATE OR REPLACE VIEW vw_menu
        AS
        SELECT a.menu_id,
            a.name,
            a.parent_menu_id,
            a.order_menu,
            a.module_id,
            a.icon,
            a.url,
            e.name AS parent_value,
            e.order_menu AS parent_order,
            d.id role_id,
            e.icon AS parent_icon,
            e.url parent_url
        FROM menu a
            JOIN modules b ON a.module_id = b.id
            JOIN module_access c ON b.id = c.module_id
            JOIN roles d ON c.role_id = d.id
            LEFT JOIN menu e ON a.parent_menu_id = e.menu_id
        WHERE c.has_access = true
        ORDER BY a.order_menu, e.order_menu;
    """)


def downgrade() -> None:
    op.execute("""
        DROP VIEW IF EXISTS vw_menu;
    """)


