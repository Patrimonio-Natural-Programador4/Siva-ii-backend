"""Actualizacion vista flujo aprobación regla condicional

Revision ID: 3bef9f3f82e7
Revises: 2aeebdfae87f
Create Date: 2026-11-25 12:33:28.643286

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3bef9f3f82e7'
down_revision: Union[str, Sequence[str], None] = '2aeebdfae87f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
CREATE OR REPLACE VIEW public.vw_approval_flows
 AS
 SELECT row_number() OVER (PARTITION BY a.approval_flow_id ORDER BY a.approval_flow_id) AS unique_id,
    a.approval_flow_id,
    a.name,
    a.description,
    a.category_id,
    b.name AS category,
    a.active AS flow_active,
    b.code AS category_code,
    c.step_id,
    c.approval_role_id,
    c.step_order,
    c.active AS step_active,
    d.name AS approval_role,
    d.active AS role_active,
    e.user_id,
    e.active AS user_role_active,
    c.assign_travel_budget,
    c.adjust_travel_itinerary,
    c.validate_supporting_documents,
    c.validate_hotel_documents,
    c.disable_advance_concepts,
    c.add_rpc,
    c.add_accounting_document,
    COALESCE(d.is_supervisor, false) AS is_supervisor,
    c.add_medical_assistance_card,
    c.add_expense_voucher,
    a.approval_with_advance,
    c.enable_payment,
    c.enable_payment_rejection,
    a.supervisor_settlement_approval,
    COALESCE(a.payment_approval, false) AS payment_approval,
    a.program_id,
    c.approved_label,
    c.adjustment_label,
    c.pending_label,
    c.assign_reviewer,
    c.enable_delegation,
	a.configuration_rules
   FROM approval_flows a
     JOIN approval_categories b ON a.category_id = b.category_id
     JOIN approval_flow_steps c ON a.approval_flow_id = c.approval_flow_id
     JOIN approval_roles d ON c.approval_role_id = d.approval_role_id
     JOIN approval_role_users e ON d.approval_role_id = e.approval_role_id;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP VIEW IF EXISTS public.vw_approval_flows;")
