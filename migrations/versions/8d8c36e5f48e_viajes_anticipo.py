"""Viajes anticipo

Revision ID: 8d8c36e5f48e
Revises: f62276e441d1
Create Date: 2026-10-07 08:32:49.046886

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d8c36e5f48e'
down_revision: Union[str, Sequence[str], None] = 'f62276e441d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
            CREATE TABLE travel_advances
            (
                travel_advance_id serial NOT NULL,
                travel_request_id integer,
                expense_advance_concept_id integer,
                amount numeric(18, 2),
                observations text,
                PRIMARY KEY (travel_advance_id),
                FOREIGN KEY (travel_request_id)
                    REFERENCES travel_requests (travel_request_id) MATCH SIMPLE
                    ON UPDATE NO ACTION
                    ON DELETE NO ACTION
                    NOT VALID,
                FOREIGN KEY (expense_advance_concept_id)
                    REFERENCES expense_advance_concepts (expense_advance_concept_id) MATCH SIMPLE
                    ON UPDATE NO ACTION
                    ON DELETE NO ACTION
                    NOT VALID
            );

            ALTER TABLE IF EXISTS travel_advances
                OWNER TO postgres;

        """)



def downgrade() -> None:
    op.execute("""
        DROP TABLE IF EXISTS travel_advances;
    """)
