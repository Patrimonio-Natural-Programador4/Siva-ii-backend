"""add_url_sharepoint_EC

Revision ID: 27d92f44f2fc
Revises: 46d5b95688fc
Create Date: 2026-09-23 13:47:45.346600

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27d92f44f2fc'
down_revision: Union[str, Sequence[str], None] = '46d5b95688fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.add_column(
       "capacity_assessments",
          sa.Column("url_sharepoint_ec", sa.Text(), nullable=True),
       
   )


def downgrade() -> None:
   op.drop_column("capacity_assessments", "url_sharepoint_ec")