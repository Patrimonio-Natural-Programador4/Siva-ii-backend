"""Ajuste vista historial aprobación

Revision ID: 688bd1f97b40
Revises: bc7cb1641323
Create Date: 2026-09-14 11:54:04.353198

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '688bd1f97b40'
down_revision: Union[str, Sequence[str], None] = 'bc7cb1641323'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        
CREATE OR REPLACE VIEW public.vw_approval_request_history
 AS
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
    --h.status AS approval_route_status,
    e.is_supervisor
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

def downgrade():
    op.execute("""
    """)
