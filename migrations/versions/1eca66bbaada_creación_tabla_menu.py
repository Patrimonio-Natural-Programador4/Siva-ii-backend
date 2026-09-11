"""Creación tabla menu

Revision ID: 1eca66bbaada
Revises: 6d6678b4db34
Create Date: 2026-09-11 03:35:00.078943

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1eca66bbaada'
down_revision: Union[str, Sequence[str], None] = '6d6678b4db34'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
            CREATE TABLE menu
            (
                menu_id serial NOT NULL,
                name text NOT NULL,
                parent_menu_id integer,
                order_menu integer,
                module_id integer,
                icon text,
                url text,
                PRIMARY KEY (menu_id),
                FOREIGN KEY (module_id)
                    REFERENCES modules (id) MATCH SIMPLE
                    ON UPDATE NO ACTION
                    ON DELETE NO ACTION
                    NOT VALID
            );
        """)



def downgrade() -> None:
    op.execute("""
        DROP TABLE IF EXISTS menu;
    """)
