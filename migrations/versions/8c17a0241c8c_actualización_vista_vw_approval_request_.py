"""Actualización vista vw_approval_request_history

Revision ID: 8c17a0241c8c
Revises: 804138dea6c7
Create Date: 2026-11-06 12:06:21.066299

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c17a0241c8c'
down_revision: Union[str, Sequence[str], None] = '804138dea6c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""

create or replace view vw_approval_request_history
as
  SELECT a.approval_request_id,
    a.related_record_id,
    a.approval_workflow_id,
    b.category_id,
    a.approval_status_id,
    c.history_id,
    c.approval_role_id,
    c.user_id,
    c.approval_status_id AS approval_status_step_id,
    c.approved_at,
    c.created_at,
        CASE
            WHEN (c.approval_status_id = ANY (ARRAY[5, 7, 8])) AND (c.comments IS NULL OR c.comments = ''::text) THEN 'Sin observaciones'::text
            ELSE c.comments
        END AS comments,
    c.step_id,
    d.step_order,
    e.name AS rol,
    (f.first_name::text || ' '::text) || f.last_name::text AS "user",
    g.name AS approval_category,
    a.guid,
    COALESCE(c.state_label, h.status) AS approval_route_status,
    e.is_supervisor,
	c.origin_user_id,
	c.origin_approval_rol_id
   FROM approval_requests a
     JOIN approval_flows b ON a.approval_workflow_id = b.approval_flow_id
     JOIN approval_request_history c ON a.approval_request_id = c.approval_request_id
     LEFT JOIN approval_flow_steps d ON c.step_id = d.step_id
     JOIN approval_roles e ON c.approval_role_id = e.approval_role_id
     LEFT JOIN users f ON c.user_id = f.id
     JOIN approval_categories g ON b.category_id = g.category_id
     JOIN approval_status h ON c.approval_status_id = h.approval_status_id
  ORDER BY a.approval_request_id DESC, d.step_order;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP VIEW IF EXISTS public.vw_approval_request_history;")
