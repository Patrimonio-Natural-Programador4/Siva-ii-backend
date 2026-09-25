# from typing import Any, Optional
# import datetime
# import decimal
# import uuid

# from sqlalchemy import ARRAY, BigInteger, Boolean, CHAR, CheckConstraint, Column, Computed, Date, DateTime, ForeignKeyConstraint, Index, Integer, JSON, LargeBinary, Numeric, PrimaryKeyConstraint, Sequence, SmallInteger, String, Table, Text, UniqueConstraint, Uuid, text
# from sqlalchemy.dialects.postgresql import CITEXT, INET, TIME, TIMESTAMP
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# class Base(DeclarativeBase):
#     pass


# class AccountTypes(Base):
#     __tablename__ = 'account_types'
#     __table_args__ = (
#         PrimaryKeyConstraint('account_type_id', name='account_types_pkey'),
#     )

#     account_type_id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     account_type: Mapped[str] = mapped_column(Text, nullable=False)


# class AgreementOrigins(Base):
#     __tablename__ = 'agreement_origins'
#     __table_args__ = (
#         CheckConstraint("color::text = ANY (ARRAY['neutral'::character varying::text, 'lime'::character varying::text, 'blue'::character varying::text, 'gray'::character varying::text, 'red'::character varying::text, 'green'::character varying::text, 'yellow'::character varying::text, 'indigo'::character varying::text, 'purple'::character varying::text, 'pink'::character varying::text, 'slate'::character varying::text, 'orange'::character varying::text, 'amber'::character varying::text, 'teal'::character varying::text, 'sky'::character varying::text])", name='agreement_origins_color_check'),
#         PrimaryKeyConstraint('id', name='agreement_origins_pkey'),
#         UniqueConstraint('name', name='agreement_origins_name_unique')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(CITEXT, nullable=False)
#     color: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'gray'::character varying"))
#     description: Mapped[Optional[str]] = mapped_column(CITEXT)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

#     agreements: Mapped[list['Agreements']] = relationship('Agreements', back_populates='agreement_origin')


# class AgreementStages(Base):
#     __tablename__ = 'agreement_stages'
#     __table_args__ = (
#         CheckConstraint("color::text = ANY (ARRAY['neutral'::character varying::text, 'lime'::character varying::text, 'blue'::character varying::text, 'gray'::character varying::text, 'red'::character varying::text, 'green'::character varying::text, 'yellow'::character varying::text, 'indigo'::character varying::text, 'purple'::character varying::text, 'pink'::character varying::text, 'slate'::character varying::text, 'orange'::character varying::text, 'amber'::character varying::text, 'teal'::character varying::text, 'sky'::character varying::text])", name='agreement_stages_color_check'),
#         ForeignKeyConstraint(['stages_id'], ['agreement_stages.id'], name='agreement_stages_stages_id_foreign'),
#         PrimaryKeyConstraint('id', name='agreement_stages_pkey')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     color: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'gray'::character varying"))
#     name: Mapped[Optional[str]] = mapped_column(CITEXT)
#     description: Mapped[Optional[str]] = mapped_column(CITEXT)
#     stages_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     stage: Mapped[Optional[str]] = mapped_column(String(255))
#     status: Mapped[Optional[str]] = mapped_column(String(255))
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     order_colum: Mapped[Optional[int]] = mapped_column(Integer)

#     stages: Mapped[Optional['AgreementStages']] = relationship('AgreementStages', remote_side=[id], back_populates='stages_reverse')
#     stages_reverse: Mapped[list['AgreementStages']] = relationship('AgreementStages', remote_side=[stages_id], back_populates='stages')
#     agreements: Mapped[list['Agreements']] = relationship('Agreements', back_populates='agreement_stage')
#     stage_rules_agreement_stage_1: Mapped[list['StageRules']] = relationship('StageRules', foreign_keys='[StageRules.agreement_stage_id_1]', back_populates='agreement_stage_1')
#     stage_rules_agreement_stage_2: Mapped[list['StageRules']] = relationship('StageRules', foreign_keys='[StageRules.agreement_stage_id_2]', back_populates='agreement_stage_2')


# class AgreementTypes(Base):
#     __tablename__ = 'agreement_types'
#     __table_args__ = (
#         CheckConstraint("color::text = ANY (ARRAY['neutral'::character varying::text, 'lime'::character varying::text, 'blue'::character varying::text, 'gray'::character varying::text, 'red'::character varying::text, 'green'::character varying::text, 'yellow'::character varying::text, 'indigo'::character varying::text, 'purple'::character varying::text, 'pink'::character varying::text, 'slate'::character varying::text, 'orange'::character varying::text, 'amber'::character varying::text, 'teal'::character varying::text, 'sky'::character varying::text])", name='agreement_types_color_check'),
#         PrimaryKeyConstraint('id', name='agreement_types_pkey'),
#         UniqueConstraint('code', name='agreement_types_code_unique'),
#         UniqueConstraint('name', name='agreement_types_name_unique'),
#         Index('agreement_types_is_independent_index', 'is_independent')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(CITEXT, nullable=False)
#     is_frame: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
#     is_independent: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
#     color: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'yellow'::character varying"))
#     code: Mapped[Optional[str]] = mapped_column(String(15))
#     description: Mapped[Optional[str]] = mapped_column(CITEXT)
#     allowed_types: Mapped[Optional[dict]] = mapped_column(JSON, comment='Permite definir si un tipo admite subtipos')
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

#     agreements: Mapped[list['Agreements']] = relationship('Agreements', back_populates='agreement_type')
#     type_rules_agreement_type_1: Mapped[list['TypeRules']] = relationship('TypeRules', foreign_keys='[TypeRules.agreement_type_id_1]', back_populates='agreement_type_1')
#     type_rules_agreement_type_2: Mapped[list['TypeRules']] = relationship('TypeRules', foreign_keys='[TypeRules.agreement_type_id_2]', back_populates='agreement_type_2')


# class ApprovalCategories(Base):
#     __tablename__ = 'approval_categories'
#     __table_args__ = (
#         PrimaryKeyConstraint('category_id', name='approval_categories_pkey'),
#     )

#     category_id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     name: Mapped[str] = mapped_column(Text, nullable=False)
#     description: Mapped[Optional[str]] = mapped_column(Text)
#     code: Mapped[Optional[str]] = mapped_column(Text)
#     active: Mapped[Optional[bool]] = mapped_column(Boolean)

#     approval_flows: Mapped[list['ApprovalFlows']] = relationship('ApprovalFlows', back_populates='category')


# class ApprovalRoles(Base):
#     __tablename__ = 'approval_roles'
#     __table_args__ = (
#         PrimaryKeyConstraint('approval_role_id', name='approval_roles_pkey'),
#     )

#     approval_role_id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     name: Mapped[str] = mapped_column(Text, nullable=False)
#     description: Mapped[Optional[str]] = mapped_column(Text)
#     active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
#     is_supervisor: Mapped[Optional[bool]] = mapped_column(Boolean)
#     fcds_employees: Mapped[Optional[bool]] = mapped_column(Boolean)
#     can_reject_payments: Mapped[Optional[bool]] = mapped_column(Boolean)

#     approval_flow_steps: Mapped[list['ApprovalFlowSteps']] = relationship('ApprovalFlowSteps', back_populates='approval_role')
#     approval_request_history: Mapped[list['ApprovalRequestHistory']] = relationship('ApprovalRequestHistory', back_populates='approval_role')
#     approval_role_users: Mapped[list['ApprovalRoleUsers']] = relationship('ApprovalRoleUsers', back_populates='approval_role')


# class ApprovalStatus(Base):
#     __tablename__ = 'approval_status'
#     __table_args__ = (
#         PrimaryKeyConstraint('approval_status_id', name='approval_status_pkey'),
#     )

#     approval_status_id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     status: Mapped[str] = mapped_column(Text, nullable=False)
#     code: Mapped[Optional[str]] = mapped_column(Text)

#     approval_requests: Mapped[list['ApprovalRequests']] = relationship('ApprovalRequests', back_populates='approval_status')
#     approval_request_history: Mapped[list['ApprovalRequestHistory']] = relationship('ApprovalRequestHistory', back_populates='approval_status')


# class Attachments(Base):
#     __tablename__ = 'attachments'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='attachments_pkey'),
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(String(255), nullable=False)
#     petition_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     extension: Mapped[Optional[str]] = mapped_column(String(255))
#     size: Mapped[Optional[str]] = mapped_column(String(255))
#     url: Mapped[Optional[str]] = mapped_column(String(255))
#     module: Mapped[Optional[str]] = mapped_column(String(255))
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))


# class Audits(Base):
#     __tablename__ = 'audits'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='audits_pkey'),
#         Index('audits_auditable_type_auditable_id_index', 'auditable_type', 'auditable_id'),
#         Index('audits_user_id_user_type_index', 'user_id', 'user_type')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     event: Mapped[str] = mapped_column(String(255), nullable=False)
#     auditable_type: Mapped[str] = mapped_column(String(255), nullable=False)
#     auditable_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     user_type: Mapped[Optional[str]] = mapped_column(String(255))
#     user_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     old_values: Mapped[Optional[str]] = mapped_column(Text)
#     new_values: Mapped[Optional[str]] = mapped_column(Text)
#     url: Mapped[Optional[str]] = mapped_column(Text)
#     ip_address: Mapped[Optional[Any]] = mapped_column(INET)
#     user_agent: Mapped[Optional[str]] = mapped_column(String(1023))
#     tags: Mapped[Optional[str]] = mapped_column(String(255))
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))


# class Banks(Base):
#     __tablename__ = 'banks'
#     __table_args__ = (
#         PrimaryKeyConstraint('bank_id', name='banks_pkey'),
#     )

#     bank_id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     bank: Mapped[str] = mapped_column(Text, nullable=False)


# class Codes(Base):
#     __tablename__ = 'codes'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='codes_pkey'),
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     code: Mapped[Optional[str]] = mapped_column(String(100))
#     origin: Mapped[Optional[str]] = mapped_column(String(100))
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

#     acquisitions: Mapped[list['Acquisitions']] = relationship('Acquisitions', back_populates='code_')
#     audit_acquisitions: Mapped[list['AuditAcquisitions']] = relationship('AuditAcquisitions', back_populates='code_')
#     lines: Mapped[list['Lines']] = relationship('Lines', back_populates='code')
#     upt_acquisitions: Mapped[list['UptAcquisitions']] = relationship('UptAcquisitions', back_populates='code_')


# class ContractTypes(Base):
#     __tablename__ = 'contract_types'
#     __table_args__ = (
#         CheckConstraint("color::text = ANY (ARRAY['neutral'::character varying::text, 'lime'::character varying::text, 'blue'::character varying::text, 'gray'::character varying::text, 'red'::character varying::text, 'green'::character varying::text, 'yellow'::character varying::text, 'indigo'::character varying::text, 'purple'::character varying::text, 'pink'::character varying::text, 'slate'::character varying::text, 'orange'::character varying::text, 'amber'::character varying::text, 'teal'::character varying::text, 'sky'::character varying::text])", name='contract_types_color_check'),
#         PrimaryKeyConstraint('id', name='contract_types_pkey'),
#         UniqueConstraint('code', name='contract_types_code_unique'),
#         UniqueConstraint('name', name='contract_types_name_unique')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(CITEXT, nullable=False)
#     color: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'gray'::character varying"))
#     code: Mapped[Optional[str]] = mapped_column(String(15))
#     description: Mapped[Optional[str]] = mapped_column(CITEXT)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

#     contracts: Mapped[list['Contracts']] = relationship('Contracts', back_populates='contract_type')


# class DisbursementState(Base):
#     __tablename__ = 'disbursement_state'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='disbursement_state_pkey'),
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(Text, nullable=False)
#     color: Mapped[Optional[str]] = mapped_column(Text)

#     disbursement: Mapped[list['Disbursement']] = relationship('Disbursement', back_populates='state')


# class DocumentTypes(Base):
#     __tablename__ = 'document_types'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='document_types_pkey'),
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(String(255), nullable=False)
#     code: Mapped[str] = mapped_column(String(255), nullable=False)
#     description: Mapped[Optional[str]] = mapped_column(String(255))
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

#     contracts: Mapped[list['Contracts']] = relationship('Contracts', back_populates='document_types')
#     implementers: Mapped[list['Implementers']] = relationship('Implementers', back_populates='document_types')
#     persons: Mapped[list['Persons']] = relationship('Persons', back_populates='document_types')
#     users: Mapped[list['Users']] = relationship('Users', back_populates='document_types')


# class ExpenseAdvanceConcepts(Base):
#     __tablename__ = 'expense_advance_concepts'
#     __table_args__ = (
#         PrimaryKeyConstraint('expense_advance_concept_id', name='advance_concepts_pkey'),
#     )

#     expense_advance_concept_id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     concept: Mapped[str] = mapped_column(Text, nullable=False)


# class ExpenseCategories(Base):
#     __tablename__ = 'expense_categories'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='expense_categories_pkey'),
#         UniqueConstraint('name', name='expense_categories_name_unique')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(CITEXT, nullable=False)
#     description: Mapped[Optional[str]] = mapped_column(CITEXT)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

#     contracts: Mapped[list['Contracts']] = relationship('Contracts', back_populates='expense_category')
#     acquisitions: Mapped[list['Acquisitions']] = relationship('Acquisitions', back_populates='expense_category')
#     audit_acquisitions: Mapped[list['AuditAcquisitions']] = relationship('AuditAcquisitions', back_populates='expense_category')
#     lines: Mapped[list['Lines']] = relationship('Lines', back_populates='expense_category')
#     upt_acquisitions: Mapped[list['UptAcquisitions']] = relationship('UptAcquisitions', back_populates='expense_category')


# class FailedJobs(Base):
#     __tablename__ = 'failed_jobs'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='failed_jobs_pkey'),
#         UniqueConstraint('uuid', name='failed_jobs_uuid_unique')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     uuid: Mapped[str] = mapped_column(String(255), nullable=False)
#     connection: Mapped[str] = mapped_column(Text, nullable=False)
#     queue: Mapped[str] = mapped_column(Text, nullable=False)
#     payload: Mapped[str] = mapped_column(Text, nullable=False)
#     exception: Mapped[str] = mapped_column(Text, nullable=False)
#     failed_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=0), nullable=False, server_default=text('CURRENT_TIMESTAMP'))


# class GeneralCategories(Base):
#     __tablename__ = 'general_categories'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='general_categories_pkey'),
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(Text, nullable=False)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

#     acquisitions: Mapped[list['Acquisitions']] = relationship('Acquisitions', back_populates='general_cat')
#     audit_acquisitions: Mapped[list['AuditAcquisitions']] = relationship('AuditAcquisitions', back_populates='general_cat')
#     upt_acquisitions: Mapped[list['UptAcquisitions']] = relationship('UptAcquisitions', back_populates='general_cat')


# class ImplementerTypes(Base):
#     __tablename__ = 'implementer_types'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='implementer_types_pkey'),
#         UniqueConstraint('name', name='implementer_types_name_unique')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(String(100), nullable=False)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

#     implementers: Mapped[list['Implementers']] = relationship('Implementers', back_populates='type')


# class Items(Base):
#     __tablename__ = 'items'
#     __table_args__ = (
#         PrimaryKeyConstraint('item_id', name='items_pkey'),
#     )

#     item_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     vdy_id: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     itm_dfncn_js: Mapped[dict] = mapped_column(JSON, nullable=False, server_default=text('\'[{"DEFINICION": [{"CAMPO": "NADA", "VALOR": "NADA"}]}]\'::jsonb'))
#     itm_rwid: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
#     itm_consec: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     itm_code: Mapped[Optional[str]] = mapped_column(String(30), server_default=text("'?'::character varying"))
#     itm_acronym: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("'?'::character varying"))
#     itm_fullname: Mapped[Optional[str]] = mapped_column(String(100), server_default=text("'?'::character varying"))
#     itm_intern_code: Mapped[Optional[str]] = mapped_column(String(30), server_default=text("'?'::character varying"))
#     itm_value: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'0'::character varying"))
#     itm_bytefile: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
#     itm_oidfile: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
#     itm_dscrpcn: Mapped[Optional[str]] = mapped_column(String(4000), server_default=text("''::character varying"))
#     itm_obsrvcn: Mapped[Optional[str]] = mapped_column(String(4000), server_default=text("''::character varying"))
#     itm_rgstatus: Mapped[Optional[str]] = mapped_column(String(2), server_default=text("'1'::character varying"))
#     aud_status: Mapped[Optional[str]] = mapped_column(String(1), server_default=text("'A'::character varying"))
#     aud_ins_user: Mapped[Optional[str]] = mapped_column(String(30), server_default=text('CURRENT_USER'))
#     aud_ins_date: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text('CURRENT_TIMESTAMP'))
#     aud_upd_user: Mapped[Optional[str]] = mapped_column(String(30), server_default=text("'S/D'::character varying"))
#     aud_upd_date: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text("to_timestamp('19000101'::text, 'YYYYMMDD'::text)"))
#     aud_vldy_ini: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text('CURRENT_TIMESTAMP'))
#     aud_vldy_fin: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text("to_timestamp('19000101'::text, 'YYYYMMDD'::text)"))


# class Jobs(Base):
#     __tablename__ = 'jobs'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='jobs_pkey'),
#         Index('jobs_queue_index', 'queue')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     queue: Mapped[str] = mapped_column(String(255), nullable=False)
#     payload: Mapped[str] = mapped_column(Text, nullable=False)
#     attempts: Mapped[int] = mapped_column(SmallInteger, nullable=False)
#     available_at: Mapped[int] = mapped_column(Integer, nullable=False)
#     created_at: Mapped[int] = mapped_column(Integer, nullable=False)
#     reserved_at: Mapped[Optional[int]] = mapped_column(Integer)


# class KfwObservations(Base):
#     __tablename__ = 'kfw_observations'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='kfw_observations_pkey'),
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(Text, nullable=False)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

#     acquisitions: Mapped[list['Acquisitions']] = relationship('Acquisitions', back_populates='kfw')
#     audit_acquisitions: Mapped[list['AuditAcquisitions']] = relationship('AuditAcquisitions', back_populates='kfw')
#     upt_acquisitions: Mapped[list['UptAcquisitions']] = relationship('UptAcquisitions', back_populates='kfw')


# class Logs(Base):
#     __tablename__ = 'logs'
#     __table_args__ = (
#         CheckConstraint("type::text = ANY (ARRAY['created'::character varying::text, 'updated'::character varying::text, 'deleted'::character varying::text])", name='logs_type_check'),
#         PrimaryKeyConstraint('id', name='logs_pkey')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     model: Mapped[str] = mapped_column(String(255), nullable=False)
#     type: Mapped[str] = mapped_column(String(255), nullable=False)
#     model_id: Mapped[Optional[str]] = mapped_column(String(255))
#     user_id: Mapped[Optional[str]] = mapped_column(String(255))
#     data: Mapped[Optional[str]] = mapped_column(Text)
#     changes: Mapped[Optional[str]] = mapped_column(Text)
#     user: Mapped[Optional[str]] = mapped_column(Text)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))


# class Migrations(Base):
#     __tablename__ = 'migrations'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='migrations_pkey'),
#     )

#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     migration: Mapped[str] = mapped_column(String(255), nullable=False)
#     batch: Mapped[int] = mapped_column(Integer, nullable=False)


# class Modalities(Base):
#     __tablename__ = 'modalities'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='modalities_pkey'),
#         UniqueConstraint('name', name='modalities_name_unique')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(String(255), nullable=False)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

#     agreements: Mapped[list['Agreements']] = relationship('Agreements', back_populates='modality')


# class Modules(Base):
#     __tablename__ = 'modules'
#     __table_args__ = (
#         CheckConstraint("type::text = ANY (ARRAY['navigation'::character varying::text, 'administration'::character varying::text, 'utils'::character varying::text])", name='modules_type_check'),
#         ForeignKeyConstraint(['module_id'], ['modules.id'], name='modules_module_id_foreign'),
#         PrimaryKeyConstraint('id', name='modules_pkey')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(CITEXT, nullable=False)
#     code: Mapped[str] = mapped_column(String(20), nullable=False)
#     type: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'link'::character varying"))
#     order: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('10'))
#     is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
#     module_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     description: Mapped[Optional[str]] = mapped_column(CITEXT)
#     route: Mapped[Optional[str]] = mapped_column(Text)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     roles: Mapped[Optional[dict]] = mapped_column(JSON)
#     permisos: Mapped[Optional[dict]] = mapped_column(JSON)

#     module: Mapped[Optional['Modules']] = relationship('Modules', remote_side=[id], back_populates='module_reverse')
#     module_reverse: Mapped[list['Modules']] = relationship('Modules', remote_side=[module_id], back_populates='module')
#     controls: Mapped[list['Controls']] = relationship('Controls', back_populates='module')
#     module_access: Mapped[list['ModuleAccess']] = relationship('ModuleAccess', back_populates='module')


# class PadHistory(Base):
#     __tablename__ = 'pad_history'
#     __table_args__ = (
#         PrimaryKeyConstraint('pdhw_id', name='pad_history_pkey'),
#     )

#     pdhw_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     pair_id: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     acquisition_id: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     vdy_id: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     plr_id: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     act_id: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     vlr_id_typ_movement: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     vlr_id_typ_category: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     vlr_id_typ_hiring: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     vlr_id_sts_hiring: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     vlr_id_typ_gnrl_ctg: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     pdhw_nmr_contract: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'))
#     cnt_id: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     prs_id_implementer: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     prs_id_executer: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     pdhw_dfncn_js: Mapped[dict] = mapped_column(JSON, nullable=False, server_default=text('\'[{"DEFINICION": [{"CAMPO": "NADA", "VALOR": "NADA"}]}]\'::jsonb'))
#     pdhw_rwid: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
#     pdhw_consec: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     pdhw_detail: Mapped[Optional[str]] = mapped_column(String(4000), server_default=text("''::character varying"))
#     pdhw_justification: Mapped[Optional[str]] = mapped_column(String(4000), server_default=text("''::character varying"))
#     pdhw_obj_bnk: Mapped[Optional[str]] = mapped_column(String(1), server_default=text("'N'::character varying"))
#     pdhw_val_budget_ini_cop: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'0'::character varying"))
#     pdhw_val_budget_ini_usd: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'0'::character varying"))
#     pdhw_val_budget_ini_eur: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'0'::character varying"))
#     pdhw_val_budget_fnl_cop: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'0'::character varying"))
#     pdhw_val_budget_fnl_usd: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'0'::character varying"))
#     pdhw_val_budget_fnl_eur: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'0'::character varying"))
#     pdhw_val_si_appropriate: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'0'::character varying"))
#     pdhw_val_no_appropriate: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'0'::character varying"))
#     pdhw_val_si_executed: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'0'::character varying"))
#     pdhw_val_no_executed: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'0'::character varying"))
#     pdhw_val_si_paid: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'0'::character varying"))
#     pdhw_val_no_paid: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'0'::character varying"))
#     pdhw_date_movement: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text("to_timestamp('19000101'::text, 'YYYYMMDD'::text)"))
#     pdhw_bytefile: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
#     pdhw_oidfile: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
#     pdhw_dscrpcn: Mapped[Optional[str]] = mapped_column(String(4000), server_default=text("''::character varying"))
#     pdhw_obsrvcn: Mapped[Optional[str]] = mapped_column(String(4000), server_default=text("''::character varying"))
#     pdhw_rgstatus: Mapped[Optional[str]] = mapped_column(String(2), server_default=text("'1'::character varying"))
#     aud_status: Mapped[Optional[str]] = mapped_column(String(1), server_default=text("'A'::character varying"))
#     aud_ins_user: Mapped[Optional[str]] = mapped_column(String(30), server_default=text('CURRENT_USER'))
#     aud_ins_date: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text('CURRENT_TIMESTAMP'))
#     aud_upd_user: Mapped[Optional[str]] = mapped_column(String(30), server_default=text("'S/D'::character varying"))
#     aud_upd_date: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text("to_timestamp('19000101'::text, 'YYYYMMDD'::text)"))
#     aud_vldy_ini: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text('CURRENT_TIMESTAMP'))
#     aud_vldy_fin: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text("to_timestamp('19000101'::text, 'YYYYMMDD'::text)"))


# class PadNews(Base):
#     __tablename__ = 'pad_news'
#     __table_args__ = (
#         PrimaryKeyConstraint('pdnw_id', name='pad_news_pkey'),
#     )

#     pdnw_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     pair_id: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     acquisition_id: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     vlr_id_typ_news: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     vlr_id_typ_cncp_bug: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     pdnw_dfncn_js: Mapped[dict] = mapped_column(JSON, nullable=False, server_default=text('\'[{"DEFINICION": [{"CAMPO": "NADA", "VALOR": "NADA"}]}]\'::jsonb'))
#     pdnw_rwid: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
#     pdnw_consec: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     pdnw_value_news: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'0'::character varying"))
#     pdnw_date_news: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text("to_timestamp('19000101'::text, 'YYYYMMDD'::text)"))
#     pdnw_detail: Mapped[Optional[str]] = mapped_column(String(4000), server_default=text("''::character varying"))
#     pdnw_justification: Mapped[Optional[str]] = mapped_column(String(4000), server_default=text("''::character varying"))
#     pdnw_bytefile: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
#     pdnw_oidfile: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
#     pdnw_dscrpcn: Mapped[Optional[str]] = mapped_column(String(4000), server_default=text("''::character varying"))
#     pdnw_obsrvcn: Mapped[Optional[str]] = mapped_column(String(4000), server_default=text("''::character varying"))
#     pdnw_rgstatus: Mapped[Optional[str]] = mapped_column(String(2), server_default=text("'1'::character varying"))
#     aud_status: Mapped[Optional[str]] = mapped_column(String(1), server_default=text("'A'::character varying"))
#     aud_ins_user: Mapped[Optional[str]] = mapped_column(String(30), server_default=text('CURRENT_USER'))
#     aud_ins_date: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text('CURRENT_TIMESTAMP'))
#     aud_upd_user: Mapped[Optional[str]] = mapped_column(String(30), server_default=text("'S/D'::character varying"))
#     aud_upd_date: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text("to_timestamp('19000101'::text, 'YYYYMMDD'::text)"))
#     aud_vldy_ini: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text('CURRENT_TIMESTAMP'))
#     aud_vldy_fin: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text("to_timestamp('19000101'::text, 'YYYYMMDD'::text)"))


# class Padpidpir(Base):
#     __tablename__ = 'padpidpir'
#     __table_args__ = (
#         PrimaryKeyConstraint('pair_id', name='padpidpir_pkey'),
#     )

#     pair_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     vdy_id: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     vlr_id_typ_srcpad: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     vlr_id_typ_color: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     pair_dfncn_js: Mapped[dict] = mapped_column(JSON, nullable=False, server_default=text('\'[{"DEFINICION": [{"CAMPO": "NADA", "VALOR": "NADA"}]}]\'::jsonb'))
#     pair_rwid: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
#     pair_consec: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     pair_code: Mapped[Optional[str]] = mapped_column(String(30), server_default=text("'?'::character varying"))
#     pair_acronym: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("'?'::character varying"))
#     pair_fullname: Mapped[Optional[str]] = mapped_column(String(100), server_default=text("'?'::character varying"))
#     pair_bytefile: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
#     pair_oidfile: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
#     pair_dscrpcn: Mapped[Optional[str]] = mapped_column(String(4000), server_default=text("''::character varying"))
#     pair_obsrvcn: Mapped[Optional[str]] = mapped_column(String(4000), server_default=text("''::character varying"))
#     pair_rgstatus: Mapped[Optional[str]] = mapped_column(String(2), server_default=text("'1'::character varying"))
#     aud_status: Mapped[Optional[str]] = mapped_column(String(1), server_default=text("'A'::character varying"))
#     aud_ins_user: Mapped[Optional[str]] = mapped_column(String(30), server_default=text('CURRENT_USER'))
#     aud_ins_date: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text('CURRENT_TIMESTAMP'))
#     aud_upd_user: Mapped[Optional[str]] = mapped_column(String(30), server_default=text("'S/D'::character varying"))
#     aud_upd_date: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text("to_timestamp('19000101'::text, 'YYYYMMDD'::text)"))
#     aud_vldy_ini: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text('CURRENT_TIMESTAMP'))
#     aud_vldy_fin: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text("to_timestamp('19000101'::text, 'YYYYMMDD'::text)"))


# class Pads(Base):
#     __tablename__ = 'pads'
#     __table_args__ = (
#         CheckConstraint("color::text = ANY (ARRAY['neutral'::character varying::text, 'lime'::character varying::text, 'blue'::character varying::text, 'gray'::character varying::text, 'red'::character varying::text, 'green'::character varying::text, 'yellow'::character varying::text, 'indigo'::character varying::text, 'purple'::character varying::text, 'pink'::character varying::text, 'slate'::character varying::text, 'orange'::character varying::text, 'amber'::character varying::text, 'teal'::character varying::text, 'sky'::character varying::text])", name='pads_color_check'),
#         PrimaryKeyConstraint('id', name='pads_pkey'),
#         UniqueConstraint('name', name='pads_name_unique')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(CITEXT, nullable=False)
#     color: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'gray'::character varying"))
#     description: Mapped[Optional[str]] = mapped_column(CITEXT)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

#     pids: Mapped[list['Pids']] = relationship('Pids', back_populates='pad_')
#     acquisitions: Mapped[list['Acquisitions']] = relationship('Acquisitions', back_populates='pad')
#     audit_acquisitions: Mapped[list['AuditAcquisitions']] = relationship('AuditAcquisitions', back_populates='pad')
#     upt_acquisitions: Mapped[list['UptAcquisitions']] = relationship('UptAcquisitions', back_populates='pad')


# class Padstatus(Base):
#     __tablename__ = 'padstatus'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='padstatus_pkey'),
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(Text, nullable=False)
#     status: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

#     acquisitions: Mapped[list['Acquisitions']] = relationship('Acquisitions', back_populates='status_')
#     audit_acquisitions: Mapped[list['AuditAcquisitions']] = relationship('AuditAcquisitions', back_populates='status_')
#     upt_acquisitions: Mapped[list['UptAcquisitions']] = relationship('UptAcquisitions', back_populates='status_')


# class PairPlanningRate(Base):
#     __tablename__ = 'pair_planning_rate'
#     __table_args__ = (
#         PrimaryKeyConstraint('pdpr_id', name='pair_planning_rate_pkey'),
#     )

#     pdpr_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     pdpr_dfncn_js: Mapped[dict] = mapped_column(JSON, nullable=False, server_default=text('\'[{"DEFINICION": [{"CAMPO": "NADA", "VALOR": "NADA"}]}]\'::jsonb'))
#     pdpr_rwid: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
#     pdpr_consec: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     pdpr_code: Mapped[Optional[str]] = mapped_column(String(15), server_default=text("'?'::character varying"))
#     pdpr_acronym: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("'?'::character varying"))
#     pdpr_fullname: Mapped[Optional[str]] = mapped_column(String(100), server_default=text("'?'::character varying"))
#     vdy_id: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     pair_id: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     cur_id: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     pdpr_value: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'0'::character varying"))
#     pdpr_bytefile: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
#     pdpr_oidfile: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
#     pdpr_dscrpcn: Mapped[Optional[str]] = mapped_column(String(4000), server_default=text("''::character varying"))
#     pdpr_obsrvcn: Mapped[Optional[str]] = mapped_column(String(4000), server_default=text("''::character varying"))
#     pdpr_rgstatus: Mapped[Optional[str]] = mapped_column(String(2), server_default=text("'1'::character varying"))
#     aud_status: Mapped[Optional[str]] = mapped_column(String(1), server_default=text("'A'::character varying"))
#     aud_ins_user: Mapped[Optional[str]] = mapped_column(String(30), server_default=text('CURRENT_USER'))
#     aud_ins_date: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text('CURRENT_TIMESTAMP'))
#     aud_upd_user: Mapped[Optional[str]] = mapped_column(String(30), server_default=text("'S/D'::character varying"))
#     aud_upd_date: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text("to_timestamp('19000101'::text, 'YYYYMMDD'::text)"))
#     aud_vldy_ini: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text('CURRENT_TIMESTAMP'))
#     aud_vldy_fin: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text("to_timestamp('19000101'::text, 'YYYYMMDD'::text)"))


# class PairsMovements(Base):
#     __tablename__ = 'pairs_movements'
#     __table_args__ = (
#         PrimaryKeyConstraint('pdmv_id', name='pairs_movements_pkey'),
#     )

#     pdmv_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     pdmv_consec: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     pair_id: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     pdpr_id_src: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     pdpr_id_rcp: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     cty_id: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     pdmv_dfncn_js: Mapped[dict] = mapped_column(JSON, nullable=False, server_default=text('\'[{"DEFINICION": [{"CAMPO": "NADA", "VALOR": "NADA"}]}]\'::jsonb'))
#     pdmv_rwid: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
#     pdmv_value_src: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'0'::character varying"))
#     pdmv_date_src: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text("to_timestamp('19000101'::text, 'YYYYMMDD'::text)"))
#     pdmv_value_rcp: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(20, 4), server_default=text("'0'::numeric"))
#     pdmv_date_rcp: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text("to_timestamp('19000101'::text, 'YYYYMMDD'::text)"))
#     pdmv_detail: Mapped[Optional[str]] = mapped_column(String(4000), server_default=text("''::character varying"))
#     pdmv_justification: Mapped[Optional[str]] = mapped_column(String(4000), server_default=text("''::character varying"))
#     pdmv_bytefile: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
#     pdmv_oidfile: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
#     pdmv_dscrpcn: Mapped[Optional[str]] = mapped_column(String(4000), server_default=text("''::character varying"))
#     pdmv_obsrvcn: Mapped[Optional[str]] = mapped_column(String(4000), server_default=text("''::character varying"))
#     pdmv_rgstatus: Mapped[Optional[str]] = mapped_column(String(2), server_default=text("'1'::character varying"))
#     aud_status: Mapped[Optional[str]] = mapped_column(String(1), server_default=text("'A'::character varying"))
#     aud_ins_user: Mapped[Optional[str]] = mapped_column(String(30), server_default=text('CURRENT_USER'))
#     aud_ins_date: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text('CURRENT_TIMESTAMP'))
#     aud_upd_user: Mapped[Optional[str]] = mapped_column(String(30), server_default=text("'S/D'::character varying"))
#     aud_upd_date: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text("to_timestamp('19000101'::text, 'YYYYMMDD'::text)"))
#     aud_vldy_ini: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text('CURRENT_TIMESTAMP'))
#     aud_vldy_fin: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0), server_default=text("to_timestamp('19000101'::text, 'YYYYMMDD'::text)"))


# t_password_resets = Table(
#     'password_resets', Base.metadata,
#     Column('email', String(255), nullable=False),
#     Column('token', String(255), nullable=False),
#     Column('created_at', TIMESTAMP(precision=0)),
#     Index('password_resets_email_index', 'email')
# )


# class Permissions(Base):
#     __tablename__ = 'permissions'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='permissions_pkey'),
#         UniqueConstraint('name', 'guard_name', name='permissions_name_guard_name_unique')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(String(255), nullable=False)
#     guard_name: Mapped[str] = mapped_column(String(255), nullable=False)
#     description: Mapped[Optional[str]] = mapped_column(String(255))
#     category: Mapped[Optional[str]] = mapped_column(String(255))
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

#     role: Mapped[list['Roles']] = relationship('Roles', secondary='role_has_permissions', back_populates='permission')
#     model_has_permissions: Mapped[list['ModelHasPermissions']] = relationship('ModelHasPermissions', back_populates='permission')


# class PersonalAccessTokens(Base):
#     __tablename__ = 'personal_access_tokens'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='personal_access_tokens_pkey'),
#         UniqueConstraint('token', name='personal_access_tokens_token_unique'),
#         Index('personal_access_tokens_tokenable_type_tokenable_id_index', 'tokenable_type', 'tokenable_id')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     tokenable_type: Mapped[str] = mapped_column(String(255), nullable=False)
#     tokenable_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     name: Mapped[str] = mapped_column(String(255), nullable=False)
#     token: Mapped[str] = mapped_column(String(64), nullable=False)
#     abilities: Mapped[Optional[str]] = mapped_column(Text)
#     last_used_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     expires_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))


# class Pillars(Base):
#     __tablename__ = 'pillars'
#     __table_args__ = (
#         CheckConstraint("color::text = ANY (ARRAY['neutral'::character varying::text, 'lime'::character varying::text, 'blue'::character varying::text, 'gray'::character varying::text, 'red'::character varying::text, 'green'::character varying::text, 'yellow'::character varying::text, 'indigo'::character varying::text, 'purple'::character varying::text, 'pink'::character varying::text, 'slate'::character varying::text, 'orange'::character varying::text, 'amber'::character varying::text, 'teal'::character varying::text, 'sky'::character varying::text])", name='pillars_color_check'),
#         PrimaryKeyConstraint('id', name='pillars_pkey'),
#         UniqueConstraint('name', name='pillars_name_unique')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(CITEXT, nullable=False)
#     color: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'gray'::character varying"))
#     description: Mapped[Optional[str]] = mapped_column(CITEXT)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

#     activities: Mapped[list['Activities']] = relationship('Activities', back_populates='pillar')
#     agreements: Mapped[list['Agreements']] = relationship('Agreements', back_populates='pillar')
#     contracts: Mapped[list['Contracts']] = relationship('Contracts', back_populates='pillar')


# class Priorities(Base):
#     __tablename__ = 'priorities'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='priorities_pkey'),
#         UniqueConstraint('level', name='priorities_level_unique'),
#         UniqueConstraint('name', name='priorities_name_unique')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(String(50), nullable=False)
#     level: Mapped[int] = mapped_column(Integer, nullable=False)
#     color: Mapped[Optional[str]] = mapped_column(String(7))
#     description: Mapped[Optional[str]] = mapped_column(Text)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

#     tasks: Mapped[list['Tasks']] = relationship('Tasks', back_populates='priority')


# class ProductsState(Base):
#     __tablename__ = 'products_state'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='products_state_pkey'),
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(Text, nullable=False)
#     color: Mapped[Optional[str]] = mapped_column(Text)

#     agreements_products: Mapped[list['AgreementsProducts']] = relationship('AgreementsProducts', back_populates='state')


# class Programs(Base):
#     __tablename__ = 'programs'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='programs_pkey'),
#         UniqueConstraint('name', name='programs_name_unique')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(CITEXT, nullable=False)
#     description: Mapped[Optional[str]] = mapped_column(CITEXT)
#     code: Mapped[Optional[str]] = mapped_column(String(100))
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

#     agreements: Mapped[list['Agreements']] = relationship('Agreements', back_populates='program')
#     approval_flows: Mapped[list['ApprovalFlows']] = relationship('ApprovalFlows', back_populates='program')
#     contracts: Mapped[list['Contracts']] = relationship('Contracts', back_populates='program')
#     travel_requests: Mapped[list['TravelRequests']] = relationship('TravelRequests', back_populates='program')
#     users_programs: Mapped[list['UsersPrograms']] = relationship('UsersPrograms', back_populates='program')


# class PurchaseTypes(Base):
#     __tablename__ = 'purchase_types'
#     __table_args__ = (
#         CheckConstraint("color::text = ANY (ARRAY['neutral'::character varying::text, 'lime'::character varying::text, 'blue'::character varying::text, 'gray'::character varying::text, 'red'::character varying::text, 'green'::character varying::text, 'yellow'::character varying::text, 'indigo'::character varying::text, 'purple'::character varying::text, 'pink'::character varying::text, 'slate'::character varying::text, 'orange'::character varying::text, 'amber'::character varying::text, 'teal'::character varying::text, 'sky'::character varying::text])", name='purchase_types_color_check'),
#         PrimaryKeyConstraint('id', name='purchase_types_pkey'),
#         UniqueConstraint('name', name='purchase_types_name_unique')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(CITEXT, nullable=False)
#     origen: Mapped[str] = mapped_column(String(255), nullable=False)
#     color: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'yellow'::character varying"))
#     description: Mapped[Optional[str]] = mapped_column(CITEXT)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

#     contracts: Mapped[list['Contracts']] = relationship('Contracts', back_populates='purchase_type')
#     acquisitions: Mapped[list['Acquisitions']] = relationship('Acquisitions', back_populates='purchase_type')
#     audit_acquisitions: Mapped[list['AuditAcquisitions']] = relationship('AuditAcquisitions', back_populates='purchase_type')
#     upt_acquisitions: Mapped[list['UptAcquisitions']] = relationship('UptAcquisitions', back_populates='purchase_type')


# class Regions(Base):
#     __tablename__ = 'regions'
#     __table_args__ = (
#         ForeignKeyConstraint(['region_id'], ['regions.id'], name='regions_region_id_foreign'),
#         PrimaryKeyConstraint('id', name='regions_pkey'),
#         UniqueConstraint('region_id', 'name', name='regions_region_id_name_unique')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     code: Mapped[str] = mapped_column(String(100), nullable=False)
#     name: Mapped[str] = mapped_column(CITEXT, nullable=False)
#     region_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     description: Mapped[Optional[str]] = mapped_column(CITEXT)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     lat: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(7, 7))
#     long: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(7, 7))

#     region: Mapped[Optional['Regions']] = relationship('Regions', remote_side=[id], back_populates='region_reverse')
#     region_reverse: Mapped[list['Regions']] = relationship('Regions', remote_side=[region_id], back_populates='region')
#     agreements: Mapped[list['Agreements']] = relationship('Agreements', back_populates='region')
#     travel_accommodations: Mapped[list['TravelAccommodations']] = relationship('TravelAccommodations', back_populates='municipality')
#     travel_itineraries_destination_municipality: Mapped[list['TravelItineraries']] = relationship('TravelItineraries', foreign_keys='[TravelItineraries.destination_municipality_id]', back_populates='destination_municipality')
#     travel_itineraries_origin_municipality: Mapped[list['TravelItineraries']] = relationship('TravelItineraries', foreign_keys='[TravelItineraries.origin_municipality_id]', back_populates='origin_municipality')


# class RequestTypes(Base):
#     __tablename__ = 'request_types'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='request_types_pkey'),
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     type: Mapped[str] = mapped_column(Text, nullable=False)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))


# class Roles(Base):
#     __tablename__ = 'roles'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='roles_pkey'),
#         UniqueConstraint('name', 'guard_name', name='roles_name_guard_name_unique')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(String(255), nullable=False)
#     guard_name: Mapped[str] = mapped_column(String(255), nullable=False)
#     description: Mapped[Optional[str]] = mapped_column(String(255))
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

#     permission: Mapped[list['Permissions']] = relationship('Permissions', secondary='role_has_permissions', back_populates='role')
#     model_has_roles: Mapped[list['ModelHasRoles']] = relationship('ModelHasRoles', back_populates='role')
#     module_access: Mapped[list['ModuleAccess']] = relationship('ModuleAccess', back_populates='role')
#     control_access: Mapped[list['ControlAccess']] = relationship('ControlAccess', back_populates='role')


# class Rubros(Base):
#     __tablename__ = 'rubros'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='rubros_pkey'),
#         UniqueConstraint('rubros', name='rubros_rubros_unique'),
#         Index('rubro_codigo', 'rubros', unique=True)
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     rubros: Mapped[str] = mapped_column(String(23), nullable=False)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     json_rubros: Mapped[Optional[dict]] = mapped_column(JSON, comment='Estructura JSON de rubros por año en formato: {"rubros": {"2025": "", "2024": "456", "2023": "1163"}}')
#     source: Mapped[Optional[str]] = mapped_column(String(50))
#     update_hws: Mapped[Optional[str]] = mapped_column(String(255))

#     acquisitions: Mapped[list['Acquisitions']] = relationship('Acquisitions', back_populates='rubro')
#     audit_acquisitions: Mapped[list['AuditAcquisitions']] = relationship('AuditAcquisitions', back_populates='rubro')
#     availabilities: Mapped[list['Availabilities']] = relationship('Availabilities', back_populates='rubro_')
#     commitments: Mapped[list['Commitments']] = relationship('Commitments', back_populates='rubro_')
#     hws: Mapped[list['Hws']] = relationship('Hws', back_populates='rubro_')
#     payment_orders: Mapped[list['PaymentOrders']] = relationship('PaymentOrders', back_populates='rubro_')
#     upt_acquisitions: Mapped[list['UptAcquisitions']] = relationship('UptAcquisitions', back_populates='rubro')
#     travel_requests: Mapped[list['TravelRequests']] = relationship('TravelRequests', back_populates='rubro')


# class StateAuditMeetingsCommittees(Base):
#     __tablename__ = 'state_audit_meetings_committees'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='state_audit_meetings_committees_pkey'),
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     state: Mapped[str] = mapped_column(Text, nullable=False)

#     audit_meetings_committees: Mapped[list['AuditMeetingsCommittees']] = relationship('AuditMeetingsCommittees', back_populates='state_audit_meetings_committees')


# class StateDetailAuditMeetingsCommittees(Base):
#     __tablename__ = 'state_detail_audit_meetings_committees'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='state_detail_audit_meetings_committees_pkey'),
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     state: Mapped[str] = mapped_column(Text, nullable=False)

#     audit_meetings_committees_detail: Mapped[list['AuditMeetingsCommitteesDetail']] = relationship('AuditMeetingsCommitteesDetail', back_populates='state_detail_audit_meetings_committees')


# class TaskStates(Base):
#     __tablename__ = 'task_states'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='task_states_pkey'),
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     task_states: Mapped[str] = mapped_column(Text, nullable=False)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

#     tasks: Mapped[list['Tasks']] = relationship('Tasks', back_populates='state')


# class TblPrueba(Base):
#     __tablename__ = 'tbl_prueba'
#     __table_args__ = (
#         CheckConstraint("COALESCE(prb_consec, '-1'::integer::bigint) > 0", name='ck_tbl_prueba_02'),
#         CheckConstraint("COALESCE(prb_id, '-1'::integer) > 0", name='ck_tbl_prueba_01'),
#         CheckConstraint("length(TRIM(BOTH FROM COALESCE(prb_code, ''::character varying))) > 0", name='ck_tbl_prueba_03'),
#         CheckConstraint("length(TRIM(BOTH FROM COALESCE(prb_name, ''::character varying))) > 0", name='ck_tbl_prueba_05'),
#         CheckConstraint("length(TRIM(BOTH FROM COALESCE(prb_sigle, ''::character varying))) > 0", name='ck_tbl_prueba_04'),
#         PrimaryKeyConstraint('prb_id', name='pk_tbl_prueba'),
#         UniqueConstraint('prb_code', name='uk_tbl_prueba_02'),
#         UniqueConstraint('prb_consec', name='uk_tbl_prueba_01'),
#         UniqueConstraint('prb_name', name='uk_tbl_prueba_04'),
#         UniqueConstraint('prb_sigle', name='uk_tbl_prueba_03')
#     )

#     prb_id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     prb_consec: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text('0'))
#     prb_code: Mapped[Optional[str]] = mapped_column(String(10), server_default=text("''::character varying"))
#     prb_sigle: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("''::character varying"))
#     prb_name: Mapped[Optional[str]] = mapped_column(String(100), server_default=text("''::character varying"))
#     prb_descrp: Mapped[Optional[str]] = mapped_column(String(4000), server_default=text("''::character varying"))
#     prb_observ: Mapped[Optional[str]] = mapped_column(String(4000), server_default=text("''::character varying"))
#     prb_state: Mapped[Optional[str]] = mapped_column(String(2), server_default=text("'A'::character varying"))
#     aud_status: Mapped[Optional[str]] = mapped_column(String(1), server_default=text("'A'::character varying"))
#     aud_ins_usr: Mapped[Optional[str]] = mapped_column(String(30), server_default=text('CURRENT_USER'))
#     aud_ins_fch: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
#     aud_upd_usr: Mapped[Optional[str]] = mapped_column(String(30), server_default=text("'S/D'::character varying"))
#     aud_upd_fch: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text("to_timestamp('19000101'::text, 'yyyymmdd'::text)"))
#     aud_vgn_ini: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
#     aud_vgn_fin: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text("to_timestamp('19000101'::text, 'yyyymmdd'::text)"))


# t_tbl_pruebados = Table(
#     'tbl_pruebados', Base.metadata,
#     Column('prb_id', Integer),
#     Column('prb_consec', BigInteger),
#     Column('prb_code', String(10)),
#     Column('prb_sigle', String(20)),
#     Column('prb_name', String(100)),
#     Column('prb_descrp', String(4000)),
#     Column('prb_observ', String(4000)),
#     Column('prb_state', String(2)),
#     Column('aud_status', String(1)),
#     Column('aud_ins_usr', String(30)),
#     Column('aud_ins_fch', DateTime),
#     Column('aud_upd_usr', String(30)),
#     Column('aud_upd_fch', DateTime),
#     Column('aud_vgn_ini', DateTime),
#     Column('aud_vgn_fin', DateTime)
# )


# class TestTable(Base):
#     __tablename__ = 'test_table'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='test_table_pkey'),
#     )

#     id: Mapped[int] = mapped_column(Integer, primary_key=True)


# class TestTable2(Base):
#     __tablename__ = 'test_table2'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='test_table2_pkey'),
#     )

#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     name: Mapped[str] = mapped_column(String(255), nullable=False)
#     observations: Mapped[str] = mapped_column(String(255), nullable=False)


# class TravelStatus(Base):
#     __tablename__ = 'travel_status'
#     __table_args__ = (
#         PrimaryKeyConstraint('status_id', name='travel_status_pkey'),
#     )

#     status_id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     name: Mapped[Optional[str]] = mapped_column(Text)

#     travel_requests: Mapped[list['TravelRequests']] = relationship('TravelRequests', back_populates='travel_status')


# class TypeAuditMeetingsCommittees(Base):
#     __tablename__ = 'type_audit_meetings_committees'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='type_audit_meetings_committees_pkey'),
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     type: Mapped[str] = mapped_column(Text, nullable=False)

#     audit_meetings_committees: Mapped[list['AuditMeetingsCommittees']] = relationship('AuditMeetingsCommittees', back_populates='type_audit_meetings_committees')


# class Units(Base):
#     __tablename__ = 'units'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='units_pkey'),
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(String(100), nullable=False)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

#     accesses: Mapped[list['Accesses']] = relationship('Accesses', back_populates='unit')


# t_vw_approval_flows = Table(
#     'vw_approval_flows', Base.metadata,
#     Column('unique_id', BigInteger),
#     Column('approval_flow_id', Integer),
#     Column('name', Text),
#     Column('description', Text),
#     Column('category_id', Integer),
#     Column('category', Text),
#     Column('flow_active', Boolean),
#     Column('category_code', Text),
#     Column('step_id', Integer),
#     Column('approval_role_id', Integer),
#     Column('step_order', Integer),
#     Column('step_active', Boolean),
#     Column('approval_role', Text),
#     Column('role_active', Boolean),
#     Column('user_id', Integer),
#     Column('user_role_active', Boolean),
#     Column('assign_travel_budget', Boolean),
#     Column('adjust_travel_itinerary', Boolean),
#     Column('validate_supporting_documents', Boolean),
#     Column('validate_hotel_documents', Boolean),
#     Column('disable_advance_concepts', Boolean),
#     Column('add_rpc', Boolean),
#     Column('add_accounting_document', Boolean),
#     Column('is_supervisor', Boolean),
#     Column('add_medical_assistance_card', Boolean),
#     Column('add_expense_voucher', Boolean),
#     Column('approval_with_advance', Boolean),
#     Column('enable_payment', Boolean),
#     Column('enable_payment_rejection', Boolean),
#     Column('supervisor_settlement_approval', Boolean),
#     Column('payment_approval', Boolean),
#     Column('program_id', Integer)
# )


# t_vw_approval_request_history = Table(
#     'vw_approval_request_history', Base.metadata,
#     Column('approval_request_id', Integer),
#     Column('related_record_id', Integer),
#     Column('approval_workflow_id', Integer),
#     Column('category_id', Integer),
#     Column('approval_status_id', Integer),
#     Column('history_id', Integer),
#     Column('approval_role_id', Integer),
#     Column('user_id', Integer),
#     Column('approval_status_step_id', Integer),
#     Column('approved_at', DateTime(True)),
#     Column('created_at', DateTime(True)),
#     Column('comments', Text),
#     Column('step_id', Integer),
#     Column('step_order', Integer),
#     Column('rol', Text),
#     Column('user', Text),
#     Column('approval_category', Text),
#     Column('guid', Uuid),
#     Column('approval_route_status', Text),
#     Column('is_supervisor', Boolean)
# )


# t_vw_role_approval_supervisor_users = Table(
#     'vw_role_approval_supervisor_users', Base.metadata,
#     Column('user_name', Text),
#     Column('user_id', BigInteger),
#     Column('approval_role_id', Integer)
# )


# class Accesses(Base):
#     __tablename__ = 'accesses'
#     __table_args__ = (
#         ForeignKeyConstraint(['unit_id'], ['units.id'], name='accesses_unit_id_foreign'),
#         PrimaryKeyConstraint('id', name='accesses_pkey'),
#         UniqueConstraint('initials', name='accesses_initials_unique'),
#         UniqueConstraint('key', name='accesses_key_unique'),
#         UniqueConstraint('name', name='accesses_name_unique')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(CITEXT, nullable=False)
#     initials: Mapped[str] = mapped_column(String(5), nullable=False)
#     key: Mapped[str] = mapped_column(String(255), nullable=False)
#     unit_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     description: Mapped[Optional[str]] = mapped_column(CITEXT)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

#     unit: Mapped['Units'] = relationship('Units', back_populates='accesses')
#     access_agreement_person: Mapped[list['AccessAgreementPerson']] = relationship('AccessAgreementPerson', back_populates='access')


# class Activities(Base):
#     __tablename__ = 'activities'
#     __table_args__ = (
#         ForeignKeyConstraint(['activity_id'], ['activities.id'], name='activities_activity_id_foreign'),
#         ForeignKeyConstraint(['pillar_id'], ['pillars.id'], name='activities_pillar_id_foreign'),
#         PrimaryKeyConstraint('id', name='activities_pkey')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     code: Mapped[str] = mapped_column(String(20), nullable=False)
#     pillar_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     activity_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     description: Mapped[Optional[str]] = mapped_column(Text)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     is_logistics_expense_associate: Mapped[Optional[bool]] = mapped_column(Boolean)

#     activity: Mapped[Optional['Activities']] = relationship('Activities', remote_side=[id], back_populates='activity_reverse')
#     activity_reverse: Mapped[list['Activities']] = relationship('Activities', remote_side=[activity_id], back_populates='activity')
#     pillar: Mapped['Pillars'] = relationship('Pillars', back_populates='activities')
#     acquisitions: Mapped[list['Acquisitions']] = relationship('Acquisitions', back_populates='activity')
#     audit_acquisitions: Mapped[list['AuditAcquisitions']] = relationship('AuditAcquisitions', back_populates='activity')
#     availabilities: Mapped[list['Availabilities']] = relationship('Availabilities', back_populates='activity')
#     commitments: Mapped[list['Commitments']] = relationship('Commitments', back_populates='activity')
#     hws: Mapped[list['Hws']] = relationship('Hws', back_populates='activity')
#     lines: Mapped[list['Lines']] = relationship('Lines', back_populates='activity')
#     payment_orders: Mapped[list['PaymentOrders']] = relationship('PaymentOrders', back_populates='activity')
#     upt_acquisitions: Mapped[list['UptAcquisitions']] = relationship('UptAcquisitions', back_populates='activity')
#     travel_requests: Mapped[list['TravelRequests']] = relationship('TravelRequests', back_populates='activity')


# class Agreements(Base):
#     __tablename__ = 'agreements'
#     __table_args__ = (
#         CheckConstraint("priority::text = ANY (ARRAY['Alto'::character varying::text, 'Medio'::character varying::text, 'Bajo'::character varying::text])", name='agreements_priority_check'),
#         ForeignKeyConstraint(['agreement_id'], ['agreements.id'], name='agreements_agreement_id_foreign'),
#         ForeignKeyConstraint(['agreement_origin_id'], ['agreement_origins.id'], name='agreements_agreement_origin_id_foreign'),
#         ForeignKeyConstraint(['agreement_stage_id'], ['agreement_stages.id'], name='agreements_agreement_stage_id_foreign'),
#         ForeignKeyConstraint(['agreement_type_id'], ['agreement_types.id'], name='agreements_agreement_type_id_foreign'),
#         ForeignKeyConstraint(['modality_id'], ['modalities.id'], ondelete='CASCADE', name='agreements_modality_id_foreign'),
#         ForeignKeyConstraint(['pillar_id'], ['pillars.id'], name='agreements_pillar_id_foreign'),
#         ForeignKeyConstraint(['program_id'], ['programs.id'], name='agreements_program_id_foreign'),
#         ForeignKeyConstraint(['region_id'], ['regions.id'], name='agreements_region_id_foreign'),
#         PrimaryKeyConstraint('id', name='agreements_pkey'),
#         UniqueConstraint('agreement_id', 'agreement_type_id', 'year', 'local', name='agreements_agreement_id_agreement_type_id_year_local_unique'),
#         UniqueConstraint('agreement_id', 'name', name='agreements_agreement_id_name_unique'),
#         Index('agreements_name_index', 'name'),
#         Index('agreements_pillar_id_index', 'pillar_id'),
#         Index('agreements_year_index', 'year')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     is_currency_usd: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
#     policy_approval: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
#     program_id: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'1'::bigint"))
#     agreement_type_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     agreement_stage_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     agreement_origin_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     name: Mapped[Optional[str]] = mapped_column(CITEXT)
#     code: Mapped[Optional[str]] = mapped_column(String(100))
#     local: Mapped[Optional[int]] = mapped_column(Integer)
#     description: Mapped[Optional[str]] = mapped_column(CITEXT)
#     value: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     year: Mapped[Optional[int]] = mapped_column(Integer)
#     request_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     finish_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     signature_fpn: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     signature_ei: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     file_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     signature_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     time_limit: Mapped[Optional[str]] = mapped_column(String(255))
#     policy_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     liquidation_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     final_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     agreement_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     pillar_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     region_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     marking: Mapped[Optional[str]] = mapped_column(String(255))
#     priority: Mapped[Optional[str]] = mapped_column(String(255), server_default=text("'Bajo'::character varying"))
#     notes: Mapped[Optional[str]] = mapped_column(Text)
#     is_valid: Mapped[Optional[bool]] = mapped_column(Boolean)
#     observations: Mapped[Optional[str]] = mapped_column(Text)
#     products: Mapped[Optional[str]] = mapped_column(Text)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     alert: Mapped[Optional[str]] = mapped_column(String(40), server_default=text('NULL::character varying'))
#     liquidation_file_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     finish_file_record_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     general_remarks: Mapped[Optional[str]] = mapped_column(Text)
#     modality_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     email_notifications: Mapped[Optional[str]] = mapped_column(String(580))
#     executed_value: Mapped[Optional[int]] = mapped_column(BigInteger)
#     financial_progress: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(20, 4))
#     summary: Mapped[Optional[str]] = mapped_column(String(5000))
#     total_value: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(45, 2))
#     financial_cutoff_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     value_executes_fpn: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     value_executes_entity: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     counterpart_execution_progress: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     ei_executed_value: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     fpn_executed_value: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     total_value_executes_FPN: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     total_value_executes_EI: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     last_report_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     contract_file_sharepoint: Mapped[Optional[str]] = mapped_column(Text)
#     shared_ei_one_drive: Mapped[Optional[str]] = mapped_column(Text)
#     shared_products_ei_one_drive: Mapped[Optional[str]] = mapped_column(Text)

#     agreement: Mapped[Optional['Agreements']] = relationship('Agreements', remote_side=[id], back_populates='agreement_reverse')
#     agreement_reverse: Mapped[list['Agreements']] = relationship('Agreements', remote_side=[agreement_id], back_populates='agreement')
#     agreement_origin: Mapped['AgreementOrigins'] = relationship('AgreementOrigins', back_populates='agreements')
#     agreement_stage: Mapped['AgreementStages'] = relationship('AgreementStages', back_populates='agreements')
#     agreement_type: Mapped['AgreementTypes'] = relationship('AgreementTypes', back_populates='agreements')
#     modality: Mapped[Optional['Modalities']] = relationship('Modalities', back_populates='agreements')
#     pillar: Mapped[Optional['Pillars']] = relationship('Pillars', back_populates='agreements')
#     program: Mapped['Programs'] = relationship('Programs', back_populates='agreements')
#     region: Mapped[Optional['Regions']] = relationship('Regions', back_populates='agreements')
#     access_agreement_person: Mapped[list['AccessAgreementPerson']] = relationship('AccessAgreementPerson', back_populates='agreement')
#     acquisitions: Mapped[list['Acquisitions']] = relationship('Acquisitions', back_populates='agreement')
#     agreement_implementer: Mapped[list['AgreementImplementer']] = relationship('AgreementImplementer', back_populates='agreement')
#     agreements_products: Mapped[list['AgreementsProducts']] = relationship('AgreementsProducts', back_populates='agreements')
#     audit_meetings_committees: Mapped[list['AuditMeetingsCommittees']] = relationship('AuditMeetingsCommittees', back_populates='agreements')
#     lines: Mapped[list['Lines']] = relationship('Lines', back_populates='agreement')
#     annotations: Mapped[list['Annotations']] = relationship('Annotations', back_populates='agreement')


# class ApprovalFlows(Base):
#     __tablename__ = 'approval_flows'
#     __table_args__ = (
#         ForeignKeyConstraint(['category_id'], ['approval_categories.category_id'], name='fk_approval_flows_category'),
#         ForeignKeyConstraint(['program_id'], ['programs.id'], name='approval_flows_program_id_fkey'),
#         PrimaryKeyConstraint('approval_flow_id', name='approval_flows_pkey'),
#         Index('idx_approval_flows_category', 'category_id')
#     )

#     approval_flow_id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     name: Mapped[str] = mapped_column(Text, nullable=False)
#     category_id: Mapped[int] = mapped_column(Integer, nullable=False)
#     description: Mapped[Optional[str]] = mapped_column(Text)
#     active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
#     approval_with_advance: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
#     supervisor_settlement_approval: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
#     payment_approval: Mapped[Optional[bool]] = mapped_column(Boolean)
#     program_id: Mapped[Optional[int]] = mapped_column(Integer)

#     category: Mapped['ApprovalCategories'] = relationship('ApprovalCategories', back_populates='approval_flows')
#     program: Mapped[Optional['Programs']] = relationship('Programs', back_populates='approval_flows')
#     approval_flow_steps: Mapped[list['ApprovalFlowSteps']] = relationship('ApprovalFlowSteps', back_populates='approval_flow')
#     approval_requests: Mapped[list['ApprovalRequests']] = relationship('ApprovalRequests', back_populates='approval_workflow')


# class Contracts(Base):
#     __tablename__ = 'contracts'
#     __table_args__ = (
#         ForeignKeyConstraint(['contract_id'], ['contracts.id'], name='contracts_contract_id_foreign'),
#         ForeignKeyConstraint(['contract_type_id'], ['contract_types.id'], name='contracts_contract_type_id_foreign'),
#         ForeignKeyConstraint(['expense_category_id'], ['expense_categories.id'], name='contracts_expense_category_id_foreign'),
#         ForeignKeyConstraint(['identification_type'], ['document_types.id'], name='contracts_identification_type_foreign'),
#         ForeignKeyConstraint(['pillar_id'], ['pillars.id'], name='contracts_pillar_id_foreign'),
#         ForeignKeyConstraint(['program_id'], ['programs.id'], name='contracts_program_id_foreign'),
#         ForeignKeyConstraint(['purchase_type_id'], ['purchase_types.id'], name='contracts_purchase_type_id_foreign'),
#         PrimaryKeyConstraint('id', name='contracts_pkey'),
#         UniqueConstraint('contract_id', 'code', name='contracts_contract_id_code_unique'),
#         Index('contracts_code_index', 'code'),
#         Index('contracts_year_index', 'year')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     code: Mapped[str] = mapped_column(String(100), nullable=False)
#     value: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     is_currency_usd: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
#     program_id: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'1'::bigint"))
#     policy_approval: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
#     description: Mapped[Optional[str]] = mapped_column(CITEXT)
#     year: Mapped[Optional[int]] = mapped_column(Integer)
#     start_contract_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     end_contract_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     identification_type: Mapped[Optional[int]] = mapped_column(BigInteger)
#     identification_number: Mapped[Optional[int]] = mapped_column(Integer)
#     bank_code: Mapped[Optional[str]] = mapped_column(String(255))
#     bank_account: Mapped[Optional[str]] = mapped_column(String(255))
#     address_line_1: Mapped[Optional[str]] = mapped_column(String(255))
#     address_line_2: Mapped[Optional[str]] = mapped_column(String(255))
#     mobile_phone: Mapped[Optional[str]] = mapped_column(String(255))
#     contract_type_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     pillar_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     expense_category_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     purchase_type_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     contract_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     observations: Mapped[Optional[str]] = mapped_column(Text)
#     policy_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     final_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     early_settlement_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     causes_early_termination: Mapped[Optional[str]] = mapped_column(Text)
#     released_resource: Mapped[Optional[int]] = mapped_column(BigInteger)

#     contract: Mapped[Optional['Contracts']] = relationship('Contracts', remote_side=[id], back_populates='contract_reverse')
#     contract_reverse: Mapped[list['Contracts']] = relationship('Contracts', remote_side=[contract_id], back_populates='contract')
#     contract_type: Mapped[Optional['ContractTypes']] = relationship('ContractTypes', back_populates='contracts')
#     expense_category: Mapped[Optional['ExpenseCategories']] = relationship('ExpenseCategories', back_populates='contracts')
#     document_types: Mapped[Optional['DocumentTypes']] = relationship('DocumentTypes', back_populates='contracts')
#     pillar: Mapped[Optional['Pillars']] = relationship('Pillars', back_populates='contracts')
#     program: Mapped['Programs'] = relationship('Programs', back_populates='contracts')
#     purchase_type: Mapped[Optional['PurchaseTypes']] = relationship('PurchaseTypes', back_populates='contracts')
#     contract_person: Mapped[list['ContractPerson']] = relationship('ContractPerson', back_populates='contract')
#     acquisition_contract: Mapped[list['AcquisitionContract']] = relationship('AcquisitionContract', back_populates='contract')
#     contract_line: Mapped[list['ContractLine']] = relationship('ContractLine', back_populates='contract')


# class Controls(Base):
#     __tablename__ = 'controls'
#     __table_args__ = (
#         ForeignKeyConstraint(['module_id'], ['modules.id'], name='fk_controls_module'),
#         PrimaryKeyConstraint('control_id', name='controls_pkey')
#     )

#     control_id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     code: Mapped[str] = mapped_column(Text, nullable=False)
#     module_id: Mapped[int] = mapped_column(Integer, nullable=False)
#     requires_validation: Mapped[Optional[bool]] = mapped_column(Boolean)

#     module: Mapped['Modules'] = relationship('Modules', back_populates='controls')
#     control_access: Mapped[list['ControlAccess']] = relationship('ControlAccess', back_populates='control')


# class Disbursement(Base):
#     __tablename__ = 'disbursement'
#     __table_args__ = (
#         ForeignKeyConstraint(['state_id'], ['disbursement_state.id'], name='fk_disbursement_state'),
#         PrimaryKeyConstraint('id', name='disbursement_pkey')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(True, 0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     value: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(15, 2))
#     scheduled_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     request_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     validation_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     approval_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     number_disbursement: Mapped[Optional[int]] = mapped_column(Integer)
#     disbursement_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     state_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     documento_soporte: Mapped[Optional[str]] = mapped_column(Text)
#     observations: Mapped[Optional[str]] = mapped_column(Text)

#     state: Mapped[Optional['DisbursementState']] = relationship('DisbursementState', back_populates='disbursement')
#     disbursement_products: Mapped[list['DisbursementProducts']] = relationship('DisbursementProducts', back_populates='disbursement')


# class Implementers(Base):
#     __tablename__ = 'implementers'
#     __table_args__ = (
#         ForeignKeyConstraint(['identification_type'], ['document_types.id'], name='implementers_identification_type_foreign'),
#         ForeignKeyConstraint(['type_id'], ['implementer_types.id'], name='implementers_type_id_foreign'),
#         PrimaryKeyConstraint('id', name='implementers_pkey'),
#         UniqueConstraint('acronym', name='implementers_acronym_unique'),
#         UniqueConstraint('identification_number', name='implementers_identification_number_unique'),
#         UniqueConstraint('name', name='implementers_name_unique')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(CITEXT, nullable=False)
#     acronym: Mapped[str] = mapped_column(CITEXT, nullable=False)
#     identification_type: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     description: Mapped[Optional[str]] = mapped_column(CITEXT)
#     identification_number: Mapped[Optional[int]] = mapped_column(BigInteger)
#     identification_dv: Mapped[Optional[int]] = mapped_column(Integer)
#     type_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     address: Mapped[Optional[str]] = mapped_column(String(120))
#     phone: Mapped[Optional[str]] = mapped_column(String(100))
#     email: Mapped[Optional[str]] = mapped_column(String(120))
#     web_page: Mapped[Optional[str]] = mapped_column(String(255))
#     is_international: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
#     manager: Mapped[Optional[str]] = mapped_column(String(255))
#     sicof_name: Mapped[Optional[str]] = mapped_column(String(225))

#     document_types: Mapped['DocumentTypes'] = relationship('DocumentTypes', back_populates='implementers')
#     type: Mapped[Optional['ImplementerTypes']] = relationship('ImplementerTypes', back_populates='implementers')
#     acquisitions_person_executer: Mapped[list['Acquisitions']] = relationship('Acquisitions', foreign_keys='[Acquisitions.person_id_executer]', back_populates='person_executer')
#     acquisitions_person_implementer: Mapped[list['Acquisitions']] = relationship('Acquisitions', foreign_keys='[Acquisitions.person_id_implementer]', back_populates='person_implementer')
#     agreement_implementer: Mapped[list['AgreementImplementer']] = relationship('AgreementImplementer', back_populates='implementer')
#     audit_acquisitions_person_executer: Mapped[list['AuditAcquisitions']] = relationship('AuditAcquisitions', foreign_keys='[AuditAcquisitions.person_id_executer]', back_populates='person_executer')
#     audit_acquisitions_person_implementer: Mapped[list['AuditAcquisitions']] = relationship('AuditAcquisitions', foreign_keys='[AuditAcquisitions.person_id_implementer]', back_populates='person_implementer')
#     lines: Mapped[list['Lines']] = relationship('Lines', back_populates='implementer')
#     upt_acquisitions_person_executer: Mapped[list['UptAcquisitions']] = relationship('UptAcquisitions', foreign_keys='[UptAcquisitions.person_id_executer]', back_populates='person_executer')
#     upt_acquisitions_person_implementer: Mapped[list['UptAcquisitions']] = relationship('UptAcquisitions', foreign_keys='[UptAcquisitions.person_id_implementer]', back_populates='person_implementer')
#     acquisition_implementer: Mapped[list['AcquisitionImplementer']] = relationship('AcquisitionImplementer', back_populates='implementer')


# class ModelHasPermissions(Base):
#     __tablename__ = 'model_has_permissions'
#     __table_args__ = (
#         ForeignKeyConstraint(['permission_id'], ['permissions.id'], ondelete='CASCADE', name='model_has_permissions_permission_id_foreign'),
#         PrimaryKeyConstraint('permission_id', 'model_id', 'model_type', name='model_has_permissions_pkey'),
#         Index('model_has_permissions_model_id_model_type_index', 'model_id', 'model_type')
#     )

#     permission_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     model_type: Mapped[str] = mapped_column(String(255), primary_key=True)
#     model_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

#     permission: Mapped['Permissions'] = relationship('Permissions', back_populates='model_has_permissions')


# class ModelHasRoles(Base):
#     __tablename__ = 'model_has_roles'
#     __table_args__ = (
#         ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE', name='model_has_roles_role_id_foreign'),
#         PrimaryKeyConstraint('role_id', 'model_id', 'model_type', name='model_has_roles_pkey'),
#         Index('model_has_roles_model_id_model_type_index', 'model_id', 'model_type')
#     )

#     role_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     model_type: Mapped[str] = mapped_column(String(255), primary_key=True)
#     model_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

#     role: Mapped['Roles'] = relationship('Roles', back_populates='model_has_roles')


# class ModuleAccess(Base):
#     __tablename__ = 'module_access'
#     __table_args__ = (
#         ForeignKeyConstraint(['module_id'], ['modules.id'], name='fk_module_access_module'),
#         ForeignKeyConstraint(['role_id'], ['roles.id'], name='fk_module_access_role'),
#         PrimaryKeyConstraint('module_access_id', name='module_access_pkey')
#     )

#     module_access_id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     role_id: Mapped[int] = mapped_column(Integer, nullable=False)
#     module_id: Mapped[int] = mapped_column(Integer, nullable=False)
#     has_access: Mapped[Optional[bool]] = mapped_column(Boolean)

#     module: Mapped['Modules'] = relationship('Modules', back_populates='module_access')
#     role: Mapped['Roles'] = relationship('Roles', back_populates='module_access')


# class Persons(Base):
#     __tablename__ = 'persons'
#     __table_args__ = (
#         ForeignKeyConstraint(['identification_type'], ['document_types.id'], name='persons_identification_type_foreign'),
#         PrimaryKeyConstraint('id', name='persons_pkey'),
#         UniqueConstraint('email', name='persons_email_unique'),
#         UniqueConstraint('former_number', name='persons_former_number_unique'),
#         UniqueConstraint('identification_number', name='persons_identification_number_unique'),
#         Index('persons_email_index', 'email'),
#         Index('persons_former_number_index', 'former_number'),
#         Index('persons_identification_number_index', 'identification_number')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     last_name: Mapped[str] = mapped_column(CITEXT, nullable=False)
#     identification_type: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     first_name: Mapped[Optional[str]] = mapped_column(CITEXT)
#     other_name: Mapped[Optional[str]] = mapped_column(CITEXT)
#     other_last_name: Mapped[Optional[str]] = mapped_column(CITEXT)
#     position: Mapped[Optional[str]] = mapped_column(CITEXT)
#     identification_number: Mapped[Optional[int]] = mapped_column(BigInteger)
#     identification_dv: Mapped[Optional[int]] = mapped_column(Integer)
#     former_number: Mapped[Optional[int]] = mapped_column(Integer)
#     former_organization_number: Mapped[Optional[int]] = mapped_column(Integer)
#     email: Mapped[Optional[str]] = mapped_column(String(255))
#     start_contract_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     end_contract_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     bank_code: Mapped[Optional[int]] = mapped_column(Integer)
#     bank_account: Mapped[Optional[str]] = mapped_column(String(255))
#     address_line_1: Mapped[Optional[str]] = mapped_column(String(255))
#     address_line_2: Mapped[Optional[str]] = mapped_column(String(255))
#     mobile_phone: Mapped[Optional[str]] = mapped_column(String(255))
#     origin: Mapped[Optional[str]] = mapped_column(String(255))
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

#     document_types: Mapped['DocumentTypes'] = relationship('DocumentTypes', back_populates='persons')
#     access_agreement_person: Mapped[list['AccessAgreementPerson']] = relationship('AccessAgreementPerson', back_populates='person')
#     contract_person: Mapped[list['ContractPerson']] = relationship('ContractPerson', back_populates='person')
#     lines: Mapped[list['Lines']] = relationship('Lines', back_populates='person')
#     users: Mapped[Optional['Users']] = relationship('Users', uselist=False, back_populates='person')


# class Pids(Base):
#     __tablename__ = 'pids'
#     __table_args__ = (
#         CheckConstraint("color::text = ANY (ARRAY['neutral'::character varying::text, 'lime'::character varying::text, 'blue'::character varying::text, 'gray'::character varying::text, 'red'::character varying::text, 'green'::character varying::text, 'yellow'::character varying::text, 'indigo'::character varying::text, 'purple'::character varying::text, 'pink'::character varying::text, 'slate'::character varying::text, 'orange'::character varying::text, 'amber'::character varying::text, 'teal'::character varying::text, 'sky'::character varying::text])", name='pids_color_check'),
#         ForeignKeyConstraint(['pad_id'], ['pads.id'], onupdate='CASCADE', name='pids_pad_id_foreign'),
#         PrimaryKeyConstraint('id', name='pids_pkey'),
#         UniqueConstraint('name', name='pids_name_unique'),
#         UniqueConstraint('pad', name='pids_pad_unique')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(CITEXT, nullable=False)
#     color: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'gray'::character varying"))
#     description: Mapped[Optional[str]] = mapped_column(CITEXT)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     eur_usd_rate: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 5), server_default=text("'0'::numeric"))
#     usd_cop_rate: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2), server_default=text("'0'::numeric"))
#     eur_cop_rate: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2), server_default=text("'0'::numeric"))
#     pad_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     pad: Mapped[Optional[str]] = mapped_column(String(255))

#     pad_: Mapped[Optional['Pads']] = relationship('Pads', back_populates='pids')
#     acquisitions: Mapped[list['Acquisitions']] = relationship('Acquisitions', back_populates='pid')
#     lines: Mapped[list['Lines']] = relationship('Lines', back_populates='pid')


# t_role_has_permissions = Table(
#     'role_has_permissions', Base.metadata,
#     Column('permission_id', BigInteger, primary_key=True),
#     Column('role_id', BigInteger, primary_key=True),
#     ForeignKeyConstraint(['permission_id'], ['permissions.id'], ondelete='CASCADE', name='role_has_permissions_permission_id_foreign'),
#     ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE', name='role_has_permissions_role_id_foreign'),
#     PrimaryKeyConstraint('permission_id', 'role_id', name='role_has_permissions_pkey')
# )


# class StageRules(Base):
#     __tablename__ = 'stage_rules'
#     __table_args__ = (
#         ForeignKeyConstraint(['agreement_stage_id_1'], ['agreement_stages.id'], name='stage_rules_agreement_stage_id_1_foreign'),
#         ForeignKeyConstraint(['agreement_stage_id_2'], ['agreement_stages.id'], name='stage_rules_agreement_stage_id_2_foreign'),
#         PrimaryKeyConstraint('id', name='stage_rules_pkey'),
#         Index('stage_rules_agreement_stage_id_1_agreement_stage_id_2_index', 'agreement_stage_id_1', 'agreement_stage_id_2')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     agreement_stage_id_2: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     agreement_stage_id_1: Mapped[Optional[int]] = mapped_column(BigInteger)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

#     agreement_stage_1: Mapped[Optional['AgreementStages']] = relationship('AgreementStages', foreign_keys=[agreement_stage_id_1], back_populates='stage_rules_agreement_stage_1')
#     agreement_stage_2: Mapped['AgreementStages'] = relationship('AgreementStages', foreign_keys=[agreement_stage_id_2], back_populates='stage_rules_agreement_stage_2')


# class TypeRules(Base):
#     __tablename__ = 'type_rules'
#     __table_args__ = (
#         ForeignKeyConstraint(['agreement_type_id_1'], ['agreement_types.id'], name='type_rules_agreement_type_id_1_foreign'),
#         ForeignKeyConstraint(['agreement_type_id_2'], ['agreement_types.id'], name='type_rules_agreement_type_id_2_foreign'),
#         PrimaryKeyConstraint('id', name='type_rules_pkey'),
#         Index('type_rules_agreement_type_id_1_agreement_type_id_2_index', 'agreement_type_id_1', 'agreement_type_id_2')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     agreement_type_id_2: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     agreement_type_id_1: Mapped[Optional[int]] = mapped_column(BigInteger)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

#     agreement_type_1: Mapped[Optional['AgreementTypes']] = relationship('AgreementTypes', foreign_keys=[agreement_type_id_1], back_populates='type_rules_agreement_type_1')
#     agreement_type_2: Mapped['AgreementTypes'] = relationship('AgreementTypes', foreign_keys=[agreement_type_id_2], back_populates='type_rules_agreement_type_2')


# class AccessAgreementPerson(Base):
#     __tablename__ = 'access_agreement_person'
#     __table_args__ = (
#         ForeignKeyConstraint(['access_id'], ['accesses.id'], name='access_agreement_person_access_id_foreign'),
#         ForeignKeyConstraint(['agreement_id'], ['agreements.id'], name='access_agreement_person_agreement_id_foreign'),
#         ForeignKeyConstraint(['person_id'], ['persons.id'], name='access_agreement_person_person_id_foreign'),
#         PrimaryKeyConstraint('id', name='access_agreement_person_pkey'),
#         UniqueConstraint('agreement_id', 'person_id', 'access_id', name='access_agreement_person_agreement_id_person_id_access_id_unique')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     agreement_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     person_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     access_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

#     access: Mapped['Accesses'] = relationship('Accesses', back_populates='access_agreement_person')
#     agreement: Mapped['Agreements'] = relationship('Agreements', back_populates='access_agreement_person')
#     person: Mapped['Persons'] = relationship('Persons', back_populates='access_agreement_person')


# class Acquisitions(Base):
#     __tablename__ = 'acquisitions'
#     __table_args__ = (
#         CheckConstraint("type::text = ANY (ARRAY['CONTRATO'::character varying, 'ACUERDO'::character varying, '0'::character varying]::text[])", name='acquisitions_type_check'),
#         ForeignKeyConstraint(['activity_id'], ['activities.id'], name='acquisitions_activity_id_foreign'),
#         ForeignKeyConstraint(['agreement_id'], ['agreements.id'], ondelete='SET NULL', onupdate='CASCADE', name='acquisitions_agreement_id_foreign'),
#         ForeignKeyConstraint(['code_id'], ['codes.id'], name='acquisitions_code_id_foreign'),
#         ForeignKeyConstraint(['expense_category_id'], ['expense_categories.id'], name='acquisitions_expense_category_id_foreign'),
#         ForeignKeyConstraint(['general_cat_id'], ['general_categories.id'], ondelete='SET NULL', onupdate='CASCADE', name='acquisitions_general_cat_id_foreign'),
#         ForeignKeyConstraint(['kfw_id'], ['kfw_observations.id'], ondelete='SET NULL', onupdate='CASCADE', name='acquisitions_kfw_id_foreign'),
#         ForeignKeyConstraint(['pad_id'], ['pads.id'], name='acquisitions_pad_id_foreign'),
#         ForeignKeyConstraint(['person_id_executer'], ['implementers.id'], ondelete='SET NULL', onupdate='CASCADE', name='acquisitions_person_id_executer_foreign'),
#         ForeignKeyConstraint(['person_id_implementer'], ['implementers.id'], ondelete='SET NULL', onupdate='CASCADE', name='acquisitions_person_id_implementer_foreign'),
#         ForeignKeyConstraint(['pid_id'], ['pids.id'], name='acquisitions_pid_id_foreign'),
#         ForeignKeyConstraint(['purchase_type_id'], ['purchase_types.id'], name='acquisitions_purchase_type_id_foreign'),
#         ForeignKeyConstraint(['rubro_id'], ['rubros.id'], ondelete='SET NULL', onupdate='CASCADE', name='acquisitions_rubro_id_foreign'),
#         ForeignKeyConstraint(['status_id'], ['padstatus.id'], ondelete='SET NULL', onupdate='CASCADE', name='acquisitions_status_id_foreign'),
#         PrimaryKeyConstraint('id', name='acquisitions_pkey')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     process_number: Mapped[int] = mapped_column(Integer, nullable=False)
#     activity_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     expense_category_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     purchase_type_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     type: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'0'::character varying"))
#     description: Mapped[Optional[str]] = mapped_column(Text)
#     numero_contrato_temporal: Mapped[Optional[str]] = mapped_column(Text)
#     pad_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     status: Mapped[Optional[str]] = mapped_column(String(255))
#     contracts_qty: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
#     trm: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(8, 2))
#     initial_budget_cop: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(20, 2), server_default=text("'0'::bigint"))
#     initial_budget_usd: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(20, 2), server_default=text("'0'::bigint"))
#     final_budget_cop: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(20, 2), server_default=text("'0'::bigint"))
#     final_budget_usd: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(20, 2), server_default=text("'0'::bigint"))
#     appropriate: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(20, 2), server_default=text("'0'::bigint"))
#     appropriate_pending: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(20, 2), server_default=text("'0'::bigint"))
#     fulfilled: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(20, 2), server_default=text("'0'::bigint"))
#     unfulfilled: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(20, 2), server_default=text("'0'::bigint"))
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     code_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     acquisition_detail: Mapped[Optional[str]] = mapped_column(Text, server_default=text("''::text"), comment='DETALLE ADQUISICIÓN')
#     vlr_id_typ_hiring: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"), comment='ID. TIPO CONTRATACIÓN (VALOR DOMINIO)')
#     vlr_id_sts_hiring: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"), comment='ID. ESTADO CONTRATACIÓN (VALOR DOMINIO)')
#     vlr_id_typ_gnrl_ctg: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"), comment='ID. TIPO CATEGORIA GENERAL (VALOR DOMINIO)')
#     contract_id: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"), comment='ID. CONTRATO SIVA')
#     paid_total_value: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(19, 4), server_default=text("'0'::numeric"), comment='MONEY type equivalent')
#     unpaid_total_value: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(19, 4), server_default=text("'0'::numeric"), comment='MONEY type equivalent')
#     detail: Mapped[Optional[str]] = mapped_column(Text)
#     code: Mapped[Optional[str]] = mapped_column(Text)
#     code_siva: Mapped[Optional[str]] = mapped_column(Text)
#     observations: Mapped[Optional[str]] = mapped_column(Text)
#     rubro_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     status_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     general_cat_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     kfw_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     person_id_implementer: Mapped[Optional[int]] = mapped_column(BigInteger)
#     person_id_executer: Mapped[Optional[int]] = mapped_column(BigInteger)
#     initial_budget_eur: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(20, 2), server_default=text("'0'::bigint"))
#     final_budget_eur: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(20, 2), server_default=text("'0'::bigint"))
#     version_creation: Mapped[Optional[str]] = mapped_column(String(255))
#     version_update: Mapped[Optional[str]] = mapped_column(String(255))
#     pid_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     cod_siva_contrato: Mapped[Optional[str]] = mapped_column(String(255))
#     cod_siva_acuerdo: Mapped[Optional[str]] = mapped_column(String(255))
#     agreement_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     contractt_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     apropiate_sicof: Mapped[Optional[int]] = mapped_column(BigInteger)
#     execute_sicof: Mapped[Optional[int]] = mapped_column(BigInteger)

#     activity: Mapped['Activities'] = relationship('Activities', back_populates='acquisitions')
#     agreement: Mapped[Optional['Agreements']] = relationship('Agreements', back_populates='acquisitions')
#     code_: Mapped[Optional['Codes']] = relationship('Codes', back_populates='acquisitions')
#     expense_category: Mapped['ExpenseCategories'] = relationship('ExpenseCategories', back_populates='acquisitions')
#     general_cat: Mapped[Optional['GeneralCategories']] = relationship('GeneralCategories', back_populates='acquisitions')
#     kfw: Mapped[Optional['KfwObservations']] = relationship('KfwObservations', back_populates='acquisitions')
#     pad: Mapped[Optional['Pads']] = relationship('Pads', back_populates='acquisitions')
#     person_executer: Mapped[Optional['Implementers']] = relationship('Implementers', foreign_keys=[person_id_executer], back_populates='acquisitions_person_executer')
#     person_implementer: Mapped[Optional['Implementers']] = relationship('Implementers', foreign_keys=[person_id_implementer], back_populates='acquisitions_person_implementer')
#     pid: Mapped[Optional['Pids']] = relationship('Pids', back_populates='acquisitions')
#     purchase_type: Mapped['PurchaseTypes'] = relationship('PurchaseTypes', back_populates='acquisitions')
#     rubro: Mapped[Optional['Rubros']] = relationship('Rubros', back_populates='acquisitions')
#     status_: Mapped[Optional['Padstatus']] = relationship('Padstatus', back_populates='acquisitions')
#     acquisition_contract: Mapped[list['AcquisitionContract']] = relationship('AcquisitionContract', back_populates='acquisition')
#     acquisition_implementer: Mapped[list['AcquisitionImplementer']] = relationship('AcquisitionImplementer', back_populates='acquisition')
#     movements_pads_destination_line: Mapped[list['MovementsPads']] = relationship('MovementsPads', foreign_keys='[MovementsPads.destination_line]', back_populates='acquisitions')
#     movements_pads_origin_line: Mapped[list['MovementsPads']] = relationship('MovementsPads', foreign_keys='[MovementsPads.origin_line]', back_populates='acquisitions_')
#     notes: Mapped[list['Notes']] = relationship('Notes', back_populates='acquisition')


# class AgreementImplementer(Base):
#     __tablename__ = 'agreement_implementer'
#     __table_args__ = (
#         ForeignKeyConstraint(['agreement_id'], ['agreements.id'], name='agreement_implementer_agreement_id_foreign'),
#         ForeignKeyConstraint(['implementer_id'], ['implementers.id'], name='agreement_implementer_implementer_id_foreign'),
#         PrimaryKeyConstraint('id', name='agreement_implementer_pkey')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     agreement_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     implementer_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     complementary_value: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     is_leading: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
#     label: Mapped[Optional[str]] = mapped_column(String(15))
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

#     agreement: Mapped['Agreements'] = relationship('Agreements', back_populates='agreement_implementer')
#     implementer: Mapped['Implementers'] = relationship('Implementers', back_populates='agreement_implementer')


# class AgreementsProducts(Base):
#     __tablename__ = 'agreements_products'
#     __table_args__ = (
#         ForeignKeyConstraint(['id_agreement'], ['agreements.id'], name='agreements_products_id_agreement_foreign'),
#         ForeignKeyConstraint(['id_product'], ['agreements_products.id'], name='fk_agreements_products'),
#         ForeignKeyConstraint(['state_id'], ['products_state.id'], name='agreements_products_state_id_foreign'),
#         PrimaryKeyConstraint('id', name='agreements_products_pkey')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     id_agreement: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     product: Mapped[str] = mapped_column(Text, nullable=False)
#     id_product: Mapped[Optional[int]] = mapped_column(BigInteger)
#     code: Mapped[Optional[str]] = mapped_column(String(255))
#     quantity: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(15, 2))
#     value: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(15, 2))
#     unit_measure: Mapped[Optional[str]] = mapped_column(Text)
#     expected_fulfillment_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     delivery_date: Mapped[Optional[datetime.time]] = mapped_column(TIME(precision=0))
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     shared_ei_one_drive: Mapped[Optional[str]] = mapped_column(Text)
#     observations: Mapped[Optional[str]] = mapped_column(Text)
#     request_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     validation_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     state_id: Mapped[Optional[int]] = mapped_column(Integer)
#     approval_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

#     agreements: Mapped['Agreements'] = relationship('Agreements', back_populates='agreements_products')
#     agreements_products: Mapped[Optional['AgreementsProducts']] = relationship('AgreementsProducts', remote_side=[id], back_populates='agreements_products_reverse')
#     agreements_products_reverse: Mapped[list['AgreementsProducts']] = relationship('AgreementsProducts', remote_side=[id_product], back_populates='agreements_products')
#     state: Mapped[Optional['ProductsState']] = relationship('ProductsState', back_populates='agreements_products')
#     disbursement_products: Mapped[list['DisbursementProducts']] = relationship('DisbursementProducts', back_populates='product')


# class ApprovalFlowSteps(Base):
#     __tablename__ = 'approval_flow_steps'
#     __table_args__ = (
#         ForeignKeyConstraint(['approval_flow_id'], ['approval_flows.approval_flow_id'], name='fk_approval_flow_steps_flow'),
#         ForeignKeyConstraint(['approval_role_id'], ['approval_roles.approval_role_id'], name='fk_approval_flow_steps_role'),
#         PrimaryKeyConstraint('step_id', name='approval_flow_steps_pkey')
#     )

#     step_id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     approval_flow_id: Mapped[int] = mapped_column(Integer, nullable=False)
#     approval_role_id: Mapped[int] = mapped_column(Integer, nullable=False)
#     step_order: Mapped[int] = mapped_column(Integer, nullable=False)
#     active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
#     request_email_cc: Mapped[Optional[str]] = mapped_column(Text)
#     adjustment_email_cc: Mapped[Optional[str]] = mapped_column(Text)
#     approval_email_cc: Mapped[Optional[str]] = mapped_column(Text)
#     assign_travel_budget: Mapped[Optional[bool]] = mapped_column(Boolean)
#     adjust_travel_itinerary: Mapped[Optional[bool]] = mapped_column(Boolean)
#     validate_supporting_documents: Mapped[Optional[bool]] = mapped_column(Boolean)
#     validate_hotel_documents: Mapped[Optional[bool]] = mapped_column(Boolean)
#     disable_advance_concepts: Mapped[Optional[bool]] = mapped_column(Boolean)
#     add_rpc: Mapped[Optional[bool]] = mapped_column(Boolean)
#     add_accounting_document: Mapped[Optional[bool]] = mapped_column(Boolean)
#     add_medical_assistance_card: Mapped[Optional[bool]] = mapped_column(Boolean)
#     add_expense_voucher: Mapped[Optional[bool]] = mapped_column(Boolean)
#     send_payment_notification: Mapped[Optional[bool]] = mapped_column(Boolean)
#     enable_payment: Mapped[Optional[bool]] = mapped_column(Boolean)
#     enable_payment_rejection: Mapped[Optional[bool]] = mapped_column(Boolean)

#     approval_flow: Mapped['ApprovalFlows'] = relationship('ApprovalFlows', back_populates='approval_flow_steps')
#     approval_role: Mapped['ApprovalRoles'] = relationship('ApprovalRoles', back_populates='approval_flow_steps')
#     approval_request_history: Mapped[list['ApprovalRequestHistory']] = relationship('ApprovalRequestHistory', back_populates='step')


# class ApprovalRequests(Base):
#     __tablename__ = 'approval_requests'
#     __table_args__ = (
#         ForeignKeyConstraint(['approval_status_id'], ['approval_status.approval_status_id'], name='fk_approval_request_status'),
#         ForeignKeyConstraint(['approval_workflow_id'], ['approval_flows.approval_flow_id'], name='fk_approval_request_workflow'),
#         PrimaryKeyConstraint('approval_request_id', name='approval_requests_pkey'),
#         Index('idx_ar_related_record', 'related_record_id'),
#         Index('idx_ar_workflow_status', 'approval_workflow_id', 'approval_status_id')
#     )

#     approval_request_id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     approval_workflow_id: Mapped[Optional[int]] = mapped_column(Integer)
#     approval_status_id: Mapped[Optional[int]] = mapped_column(Integer)
#     requester_user_id: Mapped[Optional[int]] = mapped_column(Integer)
#     name: Mapped[Optional[str]] = mapped_column(Text)
#     code: Mapped[Optional[str]] = mapped_column(Text)
#     created_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     current_step: Mapped[Optional[int]] = mapped_column(Integer)
#     related_record_id: Mapped[Optional[int]] = mapped_column(Integer)
#     instrument_code: Mapped[Optional[str]] = mapped_column(Text)
#     guid: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, server_default=text('gen_random_uuid()'))

#     approval_status: Mapped[Optional['ApprovalStatus']] = relationship('ApprovalStatus', back_populates='approval_requests')
#     approval_workflow: Mapped[Optional['ApprovalFlows']] = relationship('ApprovalFlows', back_populates='approval_requests')
#     approval_request_history: Mapped[list['ApprovalRequestHistory']] = relationship('ApprovalRequestHistory', back_populates='approval_request')


# class AuditAcquisitions(Base):
#     __tablename__ = 'audit_acquisitions'
#     __table_args__ = (
#         ForeignKeyConstraint(['activity_id'], ['activities.id'], name='audit_acquisitions_activity_id_foreign'),
#         ForeignKeyConstraint(['code_id'], ['codes.id'], name='audit_acquisitions_code_id_foreign'),
#         ForeignKeyConstraint(['expense_category_id'], ['expense_categories.id'], name='audit_acquisitions_expense_category_id_foreign'),
#         ForeignKeyConstraint(['general_cat_id'], ['general_categories.id'], ondelete='SET NULL', onupdate='CASCADE', name='audit_acquisitions_general_cat_id_foreign'),
#         ForeignKeyConstraint(['kfw_id'], ['kfw_observations.id'], ondelete='SET NULL', onupdate='CASCADE', name='audit_acquisitions_kfw_id_foreign'),
#         ForeignKeyConstraint(['pad_id'], ['pads.id'], name='audit_acquisitions_pad_id_foreign'),
#         ForeignKeyConstraint(['person_id_executer'], ['implementers.id'], ondelete='SET NULL', onupdate='CASCADE', name='audit_acquisitions_person_id_executer_foreign'),
#         ForeignKeyConstraint(['person_id_implementer'], ['implementers.id'], ondelete='SET NULL', onupdate='CASCADE', name='audit_acquisitions_person_id_implementer_foreign'),
#         ForeignKeyConstraint(['purchase_type_id'], ['purchase_types.id'], name='audit_acquisitions_purchase_type_id_foreign'),
#         ForeignKeyConstraint(['rubro_id'], ['rubros.id'], ondelete='SET NULL', onupdate='CASCADE', name='audit_acquisitions_rubro_id_foreign'),
#         ForeignKeyConstraint(['status_id'], ['padstatus.id'], ondelete='SET NULL', onupdate='CASCADE', name='audit_acquisitions_status_id_foreign'),
#         PrimaryKeyConstraint('id', name='audit_acquisitions_pkey')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     process_number: Mapped[int] = mapped_column(Integer, nullable=False)
#     pad_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     activity_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     expense_category_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     purchase_type_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     description: Mapped[Optional[str]] = mapped_column(Text)
#     numero_contrato_temporal: Mapped[Optional[str]] = mapped_column(Text)
#     status: Mapped[Optional[str]] = mapped_column(String(255))
#     contracts_qty: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
#     trm: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(8, 2))
#     initial_budget_cop: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     initial_budget_usd: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     final_budget_cop: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     final_budget_usd: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     appropriate: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     appropriate_pending: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     fulfilled: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     unfulfilled: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     detail: Mapped[Optional[str]] = mapped_column(Text)
#     code: Mapped[Optional[str]] = mapped_column(Text)
#     code_siva: Mapped[Optional[str]] = mapped_column(Text)
#     observations: Mapped[Optional[str]] = mapped_column(Text)
#     code_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     initial_budget_eur: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     final_budget_eur: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     person_id_implementer: Mapped[Optional[int]] = mapped_column(BigInteger)
#     person_id_executer: Mapped[Optional[int]] = mapped_column(BigInteger)
#     rubro_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     status_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     general_cat_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     kfw_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

#     activity: Mapped['Activities'] = relationship('Activities', back_populates='audit_acquisitions')
#     code_: Mapped[Optional['Codes']] = relationship('Codes', back_populates='audit_acquisitions')
#     expense_category: Mapped['ExpenseCategories'] = relationship('ExpenseCategories', back_populates='audit_acquisitions')
#     general_cat: Mapped[Optional['GeneralCategories']] = relationship('GeneralCategories', back_populates='audit_acquisitions')
#     kfw: Mapped[Optional['KfwObservations']] = relationship('KfwObservations', back_populates='audit_acquisitions')
#     pad: Mapped['Pads'] = relationship('Pads', back_populates='audit_acquisitions')
#     person_executer: Mapped[Optional['Implementers']] = relationship('Implementers', foreign_keys=[person_id_executer], back_populates='audit_acquisitions_person_executer')
#     person_implementer: Mapped[Optional['Implementers']] = relationship('Implementers', foreign_keys=[person_id_implementer], back_populates='audit_acquisitions_person_implementer')
#     purchase_type: Mapped['PurchaseTypes'] = relationship('PurchaseTypes', back_populates='audit_acquisitions')
#     rubro: Mapped[Optional['Rubros']] = relationship('Rubros', back_populates='audit_acquisitions')
#     status_: Mapped[Optional['Padstatus']] = relationship('Padstatus', back_populates='audit_acquisitions')


# class AuditMeetingsCommittees(Base):
#     __tablename__ = 'audit_meetings_committees'
#     __table_args__ = (
#         ForeignKeyConstraint(['id_agreement'], ['agreements.id'], name='audit_meetings_committees_id_agreement_foreign'),
#         ForeignKeyConstraint(['id_state'], ['state_audit_meetings_committees.id'], name='audit_meetings_committees_id_state_foreign'),
#         ForeignKeyConstraint(['id_type'], ['type_audit_meetings_committees.id'], name='audit_meetings_committees_id_type_foreign'),
#         PrimaryKeyConstraint('id', name='audit_meetings_committees_pkey')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     start_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     end_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     audit_firm: Mapped[Optional[str]] = mapped_column(Text)
#     scheduled_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     visit_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     report_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     id_type: Mapped[Optional[int]] = mapped_column(BigInteger)
#     attendees: Mapped[Optional[str]] = mapped_column(Text)
#     conclusions: Mapped[Optional[str]] = mapped_column(Text)
#     id_state: Mapped[Optional[int]] = mapped_column(BigInteger)
#     id_agreement: Mapped[Optional[int]] = mapped_column(BigInteger)
#     execution_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     agenda: Mapped[Optional[str]] = mapped_column(Text)
#     meeting_proceedings: Mapped[Optional[str]] = mapped_column(Text)
#     location: Mapped[Optional[str]] = mapped_column(Text)
#     committee_meet_number: Mapped[Optional[int]] = mapped_column(BigInteger)
#     support_link: Mapped[Optional[str]] = mapped_column(Text)
#     recording_link: Mapped[Optional[str]] = mapped_column(Text)

#     agreements: Mapped[Optional['Agreements']] = relationship('Agreements', back_populates='audit_meetings_committees')
#     state_audit_meetings_committees: Mapped[Optional['StateAuditMeetingsCommittees']] = relationship('StateAuditMeetingsCommittees', back_populates='audit_meetings_committees')
#     type_audit_meetings_committees: Mapped[Optional['TypeAuditMeetingsCommittees']] = relationship('TypeAuditMeetingsCommittees', back_populates='audit_meetings_committees')
#     audit_meetings_committees_detail: Mapped[list['AuditMeetingsCommitteesDetail']] = relationship('AuditMeetingsCommitteesDetail', back_populates='audit_meetings_committees')


# class Availabilities(Base):
#     __tablename__ = 'availabilities'
#     __table_args__ = (
#         CheckConstraint("description1::text = ANY (ARRAY['ANULADA'::character varying, 'APROBADA'::character varying]::text[])", name='availabilities_description1_check'),
#         ForeignKeyConstraint(['activity_id'], ['activities.id'], ondelete='SET NULL', onupdate='CASCADE', name='availabilities_activity_id_foreign'),
#         ForeignKeyConstraint(['rubro_id'], ['rubros.id'], ondelete='SET NULL', onupdate='CASCADE', name='availabilities_rubro_id_foreign'),
#         PrimaryKeyConstraint('id', name='availabilities_pkey')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     consecutive: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     preparation_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
#     approval_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
#     total_item_value: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     total_commitment: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     item_balance: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     total_cancelled: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     description1: Mapped[str] = mapped_column(String(255), nullable=False)
#     value_to_cancell: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     description2: Mapped[str] = mapped_column(Text, nullable=False)
#     summary_code: Mapped[int] = mapped_column(Integer, nullable=False)
#     rubro_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     project_name: Mapped[str] = mapped_column(Text, nullable=False)
#     activity_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     apropiation: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     total_addition: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     total_deductions: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     total_credit: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     total_countercredit: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     final_budget: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     total_availability: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     total_commitments: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     total_payment_orders: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     total_reimbursement: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     available: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     total_advances: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     total_amortized: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     validity_year: Mapped[int] = mapped_column(Integer, nullable=False)
#     rubro: Mapped[str] = mapped_column(String(23), nullable=False)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

#     activity: Mapped['Activities'] = relationship('Activities', back_populates='availabilities')
#     rubro_: Mapped['Rubros'] = relationship('Rubros', back_populates='availabilities')


# class Commitments(Base):
#     __tablename__ = 'commitments'
#     __table_args__ = (
#         CheckConstraint("description1::text = ANY (ARRAY['ANULADO'::character varying, 'APROBADO'::character varying]::text[])", name='commitments_description1_check'),
#         ForeignKeyConstraint(['activity_id'], ['activities.id'], ondelete='SET NULL', onupdate='CASCADE', name='commitments_activity_id_foreign'),
#         ForeignKeyConstraint(['rubro_id'], ['rubros.id'], ondelete='SET NULL', onupdate='CASCADE', name='commitments_rubro_id_foreign'),
#         PrimaryKeyConstraint('id', name='commitments_pkey')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     sequence_number: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     creation_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
#     approval_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
#     availability: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     total_value: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     total_received: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     total_paid: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     total_ordered: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     description1: Mapped[str] = mapped_column(String(255), nullable=False)
#     balance: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     nit: Mapped[decimal.Decimal] = mapped_column(Numeric(20, 1), nullable=False)
#     name: Mapped[str] = mapped_column(Text, nullable=False)
#     total_advance_payment: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     total_amortized: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     total_write_off: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     short_code: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     rubro_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     project_name: Mapped[str] = mapped_column(Text, nullable=False)
#     activity_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     contract: Mapped[str] = mapped_column(Text, nullable=False)
#     secop_contract_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     description2: Mapped[str] = mapped_column(Text, nullable=False)
#     year: Mapped[int] = mapped_column(Integer, nullable=False)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     rubro: Mapped[Optional[str]] = mapped_column(String(23))

#     activity: Mapped['Activities'] = relationship('Activities', back_populates='commitments')
#     rubro_: Mapped['Rubros'] = relationship('Rubros', back_populates='commitments')


# class ContractPerson(Base):
#     __tablename__ = 'contract_person'
#     __table_args__ = (
#         ForeignKeyConstraint(['contract_id'], ['contracts.id'], name='contract_person_contract_id_foreign'),
#         ForeignKeyConstraint(['person_id'], ['persons.id'], name='contract_person_person_id_foreign'),
#         PrimaryKeyConstraint('id', name='contract_person_pkey'),
#         UniqueConstraint('contract_id', 'person_id', name='contract_person_contract_id_person_id_unique')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     contract_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     person_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     type_id: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'Contratista'::character varying"))
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

#     contract: Mapped['Contracts'] = relationship('Contracts', back_populates='contract_person')
#     person: Mapped['Persons'] = relationship('Persons', back_populates='contract_person')


# class ControlAccess(Base):
#     __tablename__ = 'control_access'
#     __table_args__ = (
#         ForeignKeyConstraint(['control_id'], ['controls.control_id'], name='fk_control_access_control'),
#         ForeignKeyConstraint(['role_id'], ['roles.id'], name='fk_control_access_role'),
#         PrimaryKeyConstraint('control_access_id', name='control_access_pkey')
#     )

#     control_access_id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     role_id: Mapped[Optional[int]] = mapped_column(Integer)
#     control_id: Mapped[Optional[int]] = mapped_column(Integer)
#     has_access: Mapped[Optional[bool]] = mapped_column(Boolean)

#     control: Mapped[Optional['Controls']] = relationship('Controls', back_populates='control_access')
#     role: Mapped[Optional['Roles']] = relationship('Roles', back_populates='control_access')


# class Hws(Base):
#     __tablename__ = 'hws'
#     __table_args__ = (
#         ForeignKeyConstraint(['activity_id'], ['activities.id'], ondelete='SET NULL', onupdate='CASCADE', name='hws_activity_id_foreign'),
#         ForeignKeyConstraint(['rubro_id'], ['rubros.id'], ondelete='SET NULL', onupdate='CASCADE', name='hws_rubro_id_foreign'),
#         PrimaryKeyConstraint('id', name='hws_pkey')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     code1: Mapped[str] = mapped_column(String(255), nullable=False)
#     code2: Mapped[str] = mapped_column(String(255), nullable=False)
#     code3: Mapped[str] = mapped_column(String(255), nullable=False)
#     code4: Mapped[int] = mapped_column(Integer, nullable=False)
#     code5: Mapped[int] = mapped_column(Integer, nullable=False)
#     code6: Mapped[str] = mapped_column(String(255), nullable=False)
#     description1: Mapped[str] = mapped_column(String(255), nullable=False)
#     description2: Mapped[str] = mapped_column(String(255), nullable=False)
#     description3: Mapped[str] = mapped_column(String(255), nullable=False)
#     description4: Mapped[str] = mapped_column(String(255), nullable=False)
#     description5: Mapped[str] = mapped_column(String(255), nullable=False)
#     description6: Mapped[str] = mapped_column(String(255), nullable=False)
#     project_name: Mapped[str] = mapped_column(Text, nullable=False)
#     activity_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     rubro_code: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     summary_code: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     rubro_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     apropiation: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     final: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     ordinations: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     availability: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     available: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     execution: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     commitments: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     to_be_executed: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     pays: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     available_balance: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     year: Mapped[int] = mapped_column(Integer, nullable=False)
#     rubro: Mapped[str] = mapped_column(String(255), nullable=False)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

#     activity: Mapped['Activities'] = relationship('Activities', back_populates='hws')
#     rubro_: Mapped['Rubros'] = relationship('Rubros', back_populates='hws')


# class Lines(Base):
#     __tablename__ = 'lines'
#     __table_args__ = (
#         ForeignKeyConstraint(['activity_id'], ['activities.id'], name='lines_activity_id_foreign'),
#         ForeignKeyConstraint(['agreement_id'], ['agreements.id'], name='lines_agreement_id_foreign'),
#         ForeignKeyConstraint(['code_id'], ['codes.id'], name='lines_code_id_foreign'),
#         ForeignKeyConstraint(['expense_category_id'], ['expense_categories.id'], name='lines_expense_category_id_foreign'),
#         ForeignKeyConstraint(['implementer_id'], ['implementers.id'], name='lines_implementer_id_foreign'),
#         ForeignKeyConstraint(['line_id'], ['lines.id'], name='lines_line_id_foreign'),
#         ForeignKeyConstraint(['person_id'], ['persons.id'], name='lines_person_id_foreign'),
#         ForeignKeyConstraint(['pid_id'], ['pids.id'], name='lines_pid_id_foreign'),
#         PrimaryKeyConstraint('id', name='lines_pkey')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     agreement_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     description: Mapped[str] = mapped_column(CITEXT, nullable=False)
#     line_number: Mapped[int] = mapped_column(Integer, nullable=False)
#     activity_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     pid_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     num_linea_paa: Mapped[str] = mapped_column(String(50), nullable=False)
#     appropriate_value: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     is_currency_usd: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
#     is_managed: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
#     expense_category_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     line_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     implementer_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     otrosi: Mapped[Optional[str]] = mapped_column(String(50))
#     settle_value: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     accomplished_value: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     observations: Mapped[Optional[str]] = mapped_column(Text)
#     code_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     person_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     paa_version: Mapped[Optional[str]] = mapped_column(String(255))

#     activity: Mapped['Activities'] = relationship('Activities', back_populates='lines')
#     agreement: Mapped['Agreements'] = relationship('Agreements', back_populates='lines')
#     code: Mapped[Optional['Codes']] = relationship('Codes', back_populates='lines')
#     expense_category: Mapped['ExpenseCategories'] = relationship('ExpenseCategories', back_populates='lines')
#     implementer: Mapped[Optional['Implementers']] = relationship('Implementers', back_populates='lines')
#     line: Mapped[Optional['Lines']] = relationship('Lines', remote_side=[id], back_populates='line_reverse')
#     line_reverse: Mapped[list['Lines']] = relationship('Lines', remote_side=[line_id], back_populates='line')
#     person: Mapped[Optional['Persons']] = relationship('Persons', back_populates='lines')
#     pid: Mapped['Pids'] = relationship('Pids', back_populates='lines')
#     contract_line: Mapped[list['ContractLine']] = relationship('ContractLine', back_populates='line')


# class PaymentOrders(Base):
#     __tablename__ = 'payment_orders'
#     __table_args__ = (
#         ForeignKeyConstraint(['activity_id'], ['activities.id'], ondelete='SET NULL', onupdate='CASCADE', name='payment_orders_activity_id_foreign'),
#         ForeignKeyConstraint(['rubro_id'], ['rubros.id'], ondelete='SET NULL', onupdate='CASCADE', name='payment_orders_rubro_id_foreign'),
#         PrimaryKeyConstraint('id', name='payment_orders_pkey')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     consecutive: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     consecutive_rp: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     date_prepared: Mapped[datetime.date] = mapped_column(Date, nullable=False)
#     approval_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
#     notes: Mapped[str] = mapped_column(Text, nullable=False)
#     op_value: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     nit: Mapped[decimal.Decimal] = mapped_column(Numeric(20, 1), nullable=False)
#     name: Mapped[str] = mapped_column(Text, nullable=False)
#     summary_code: Mapped[int] = mapped_column(Integer, nullable=False)
#     rubro_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     project_name: Mapped[str] = mapped_column(Text, nullable=False)
#     activity_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     pays: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     year: Mapped[int] = mapped_column(Integer, nullable=False)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     rubro: Mapped[Optional[str]] = mapped_column(String(23))

#     activity: Mapped['Activities'] = relationship('Activities', back_populates='payment_orders')
#     rubro_: Mapped['Rubros'] = relationship('Rubros', back_populates='payment_orders')


# class UptAcquisitions(Base):
#     __tablename__ = 'upt_acquisitions'
#     __table_args__ = (
#         ForeignKeyConstraint(['activity_id'], ['activities.id'], name='upt_acquisitions_activity_id_foreign'),
#         ForeignKeyConstraint(['code_id'], ['codes.id'], name='upt_acquisitions_code_id_foreign'),
#         ForeignKeyConstraint(['expense_category_id'], ['expense_categories.id'], name='upt_acquisitions_expense_category_id_foreign'),
#         ForeignKeyConstraint(['general_cat_id'], ['general_categories.id'], ondelete='SET NULL', onupdate='CASCADE', name='upt_acquisitions_general_cat_id_foreign'),
#         ForeignKeyConstraint(['kfw_id'], ['kfw_observations.id'], ondelete='SET NULL', onupdate='CASCADE', name='upt_acquisitions_kfw_id_foreign'),
#         ForeignKeyConstraint(['pad_id'], ['pads.id'], name='upt_acquisitions_pad_id_foreign'),
#         ForeignKeyConstraint(['person_id_executer'], ['implementers.id'], ondelete='SET NULL', onupdate='CASCADE', name='upt_acquisitions_person_id_executer_foreign'),
#         ForeignKeyConstraint(['person_id_implementer'], ['implementers.id'], ondelete='SET NULL', onupdate='CASCADE', name='upt_acquisitions_person_id_implementer_foreign'),
#         ForeignKeyConstraint(['purchase_type_id'], ['purchase_types.id'], name='upt_acquisitions_purchase_type_id_foreign'),
#         ForeignKeyConstraint(['rubro_id'], ['rubros.id'], ondelete='SET NULL', onupdate='CASCADE', name='upt_acquisitions_rubro_id_foreign'),
#         ForeignKeyConstraint(['status_id'], ['padstatus.id'], ondelete='SET NULL', onupdate='CASCADE', name='upt_acquisitions_status_id_foreign'),
#         PrimaryKeyConstraint('id', name='upt_acquisitions_pkey')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     id_adquisition: Mapped[int] = mapped_column(Integer, nullable=False)
#     process_number: Mapped[int] = mapped_column(Integer, nullable=False)
#     pad_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     activity_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     expense_category_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     purchase_type_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     description: Mapped[Optional[str]] = mapped_column(Text)
#     numero_contrato_temporal: Mapped[Optional[str]] = mapped_column(Text)
#     status: Mapped[Optional[str]] = mapped_column(String(255))
#     contracts_qty: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
#     trm: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(8, 2))
#     initial_budget_cop: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     initial_budget_usd: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     final_budget_cop: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     final_budget_usd: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     appropriate: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     appropriate_pending: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     fulfilled: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     unfulfilled: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     detail: Mapped[Optional[str]] = mapped_column(Text)
#     code: Mapped[Optional[str]] = mapped_column(Text)
#     code_siva: Mapped[Optional[str]] = mapped_column(Text)
#     observations: Mapped[Optional[str]] = mapped_column(Text)
#     code_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     initial_budget_eur: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     final_budget_eur: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text("'0'::bigint"))
#     person_id_implementer: Mapped[Optional[int]] = mapped_column(BigInteger)
#     person_id_executer: Mapped[Optional[int]] = mapped_column(BigInteger)
#     rubro_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     status_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     general_cat_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     kfw_id: Mapped[Optional[int]] = mapped_column(BigInteger)

#     activity: Mapped['Activities'] = relationship('Activities', back_populates='upt_acquisitions')
#     code_: Mapped[Optional['Codes']] = relationship('Codes', back_populates='upt_acquisitions')
#     expense_category: Mapped['ExpenseCategories'] = relationship('ExpenseCategories', back_populates='upt_acquisitions')
#     general_cat: Mapped[Optional['GeneralCategories']] = relationship('GeneralCategories', back_populates='upt_acquisitions')
#     kfw: Mapped[Optional['KfwObservations']] = relationship('KfwObservations', back_populates='upt_acquisitions')
#     pad: Mapped['Pads'] = relationship('Pads', back_populates='upt_acquisitions')
#     person_executer: Mapped[Optional['Implementers']] = relationship('Implementers', foreign_keys=[person_id_executer], back_populates='upt_acquisitions_person_executer')
#     person_implementer: Mapped[Optional['Implementers']] = relationship('Implementers', foreign_keys=[person_id_implementer], back_populates='upt_acquisitions_person_implementer')
#     purchase_type: Mapped['PurchaseTypes'] = relationship('PurchaseTypes', back_populates='upt_acquisitions')
#     rubro: Mapped[Optional['Rubros']] = relationship('Rubros', back_populates='upt_acquisitions')
#     status_: Mapped[Optional['Padstatus']] = relationship('Padstatus', back_populates='upt_acquisitions')


# class Users(Base):
#     __tablename__ = 'users'
#     __table_args__ = (
#         ForeignKeyConstraint(['identification_type'], ['document_types.id'], name='users_identification_type_foreign'),
#         ForeignKeyConstraint(['person_id'], ['persons.id'], name='users_person_id_foreign'),
#         PrimaryKeyConstraint('id', name='users_pkey'),
#         UniqueConstraint('email', name='users_email_unique'),
#         UniqueConstraint('identification_number', name='users_identification_number_unique'),
#         UniqueConstraint('person_id', name='users_person_id_unique'),
#         Index('users_email_index', 'email'),
#         Index('users_identification_number_index', 'identification_number')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     first_name: Mapped[str] = mapped_column(CITEXT, nullable=False)
#     last_name: Mapped[str] = mapped_column(CITEXT, nullable=False)
#     identification_type: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     identification_number: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     email: Mapped[str] = mapped_column(String(255), nullable=False)
#     is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
#     guid: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, server_default=text('gen_random_uuid()'))
#     other_name: Mapped[Optional[str]] = mapped_column(CITEXT)
#     other_last_name: Mapped[Optional[str]] = mapped_column(CITEXT)
#     position: Mapped[Optional[str]] = mapped_column(CITEXT)
#     email_verified_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     password: Mapped[Optional[str]] = mapped_column(String(255))
#     mobile_phone: Mapped[Optional[str]] = mapped_column(String(255))
#     remember_token: Mapped[Optional[str]] = mapped_column(String(100))
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     person_id: Mapped[Optional[int]] = mapped_column(Integer)
#     guid_msft: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
#     full_name: Mapped[Optional[str]] = mapped_column(Text, Computed("TRIM(BOTH FROM (((((((COALESCE(first_name, ''::citext))::text || ' '::text) || (COALESCE(other_name, ''::citext))::text) || ' '::text) || (COALESCE(last_name, ''::citext))::text) || ' '::text) || (COALESCE(other_last_name, ''::citext))::text))", persisted=True))
#     is_guest: Mapped[Optional[bool]] = mapped_column(Boolean)

#     document_types: Mapped['DocumentTypes'] = relationship('DocumentTypes', back_populates='users')
#     person: Mapped[Optional['Persons']] = relationship('Persons', back_populates='users')
#     annotations: Mapped[list['Annotations']] = relationship('Annotations', back_populates='user')
#     approval_role_users: Mapped[list['ApprovalRoleUsers']] = relationship('ApprovalRoleUsers', back_populates='user')
#     notifications: Mapped[list['Notifications']] = relationship('Notifications', back_populates='user')
#     tasks_applicant: Mapped[list['Tasks']] = relationship('Tasks', foreign_keys='[Tasks.applicant_id]', back_populates='applicant')
#     tasks_executor: Mapped[list['Tasks']] = relationship('Tasks', foreign_keys='[Tasks.executor_id]', back_populates='executor')
#     tasks_responsible: Mapped[list['Tasks']] = relationship('Tasks', foreign_keys='[Tasks.responsible_id]', back_populates='responsible')
#     tasks_reviewer: Mapped[list['Tasks']] = relationship('Tasks', foreign_keys='[Tasks.reviewer_id]', back_populates='reviewer')
#     travel_requests: Mapped[list['TravelRequests']] = relationship('TravelRequests', back_populates='traveler_user')
#     users_programs: Mapped[list['UsersPrograms']] = relationship('UsersPrograms', back_populates='user')
#     observations: Mapped[list['Observations']] = relationship('Observations', back_populates='users')


# class AcquisitionContract(Base):
#     __tablename__ = 'acquisition_contract'
#     __table_args__ = (
#         ForeignKeyConstraint(['acquisition_id'], ['acquisitions.id'], name='acquisition_contract_acquisition_id_foreign'),
#         ForeignKeyConstraint(['contract_id'], ['contracts.id'], name='acquisition_contract_contract_id_foreign'),
#         PrimaryKeyConstraint('id', name='acquisition_contract_pkey'),
#         UniqueConstraint('acquisition_id', 'contract_id', name='acquisition_contract_acquisition_id_contract_id_unique')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     acquisition_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     contract_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

#     acquisition: Mapped['Acquisitions'] = relationship('Acquisitions', back_populates='acquisition_contract')
#     contract: Mapped['Contracts'] = relationship('Contracts', back_populates='acquisition_contract')


# class AcquisitionImplementer(Base):
#     __tablename__ = 'acquisition_implementer'
#     __table_args__ = (
#         CheckConstraint("role::text = ANY (ARRAY['implementadora'::character varying::text, 'ejecutora'::character varying::text])", name='acquisition_implementer_role_check'),
#         ForeignKeyConstraint(['acquisition_id'], ['acquisitions.id'], name='acquisition_implementer_acquisition_id_foreign'),
#         ForeignKeyConstraint(['implementer_id'], ['implementers.id'], name='acquisition_implementer_implementer_id_foreign'),
#         PrimaryKeyConstraint('id', name='acquisition_implementer_pkey'),
#         UniqueConstraint('acquisition_id', 'implementer_id', 'role', name='acquisition_implementer_acquisition_id_implementer_id_role_uniq')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     acquisition_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     implementer_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     role: Mapped[str] = mapped_column(String(255), nullable=False)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

#     acquisition: Mapped['Acquisitions'] = relationship('Acquisitions', back_populates='acquisition_implementer')
#     implementer: Mapped['Implementers'] = relationship('Implementers', back_populates='acquisition_implementer')


# class Annotations(Base):
#     __tablename__ = 'annotations'
#     __table_args__ = (
#         ForeignKeyConstraint(['agreement_id'], ['agreements.id'], ondelete='CASCADE', name='annotations_agreement_id_foreign'),
#         ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='annotations_user_id_foreign'),
#         PrimaryKeyConstraint('id', name='annotations_pkey')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     name: Mapped[str] = mapped_column(CITEXT, nullable=False)
#     is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
#     agreement_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     annotated_at: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     description: Mapped[Optional[str]] = mapped_column(CITEXT)
#     user_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

#     agreement: Mapped['Agreements'] = relationship('Agreements', back_populates='annotations')
#     user: Mapped[Optional['Users']] = relationship('Users', back_populates='annotations')


# class ApprovalRequestHistory(Base):
#     __tablename__ = 'approval_request_history'
#     __table_args__ = (
#         ForeignKeyConstraint(['approval_request_id'], ['approval_requests.approval_request_id'], name='fk_approval_request_history_request'),
#         ForeignKeyConstraint(['approval_role_id'], ['approval_roles.approval_role_id'], name='fk_approval_request_history_role'),
#         ForeignKeyConstraint(['approval_status_id'], ['approval_status.approval_status_id'], name='fk_approval_request_history_status'),
#         ForeignKeyConstraint(['step_id'], ['approval_flow_steps.step_id'], name='fk_approval_request_history_route'),
#         PrimaryKeyConstraint('history_id', name='approval_request_history_pkey'),
#         Index('idx_arh_request', 'approval_request_id'),
#         Index('idx_arh_role', 'approval_role_id'),
#         Index('idx_arh_status_user', 'approval_status_id', 'user_id'),
#         Index('idx_arh_user_status', 'user_id', 'approval_status_id')
#     )

#     history_id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     approval_request_id: Mapped[int] = mapped_column(Integer, nullable=False)
#     approval_role_id: Mapped[int] = mapped_column(Integer, nullable=False)
#     approval_status_id: Mapped[int] = mapped_column(Integer, nullable=False)
#     user_id: Mapped[Optional[int]] = mapped_column(Integer)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
#     comments: Mapped[Optional[str]] = mapped_column(Text)
#     step_id: Mapped[Optional[int]] = mapped_column(Integer)
#     approved_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
#     received_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
#     due_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
#     mentioned_user_ids: Mapped[Optional[list[int]]] = mapped_column(ARRAY(Integer()))
#     approver_user_id: Mapped[Optional[int]] = mapped_column(Integer)
#     approved_by_user: Mapped[Optional[str]] = mapped_column(Text)

#     approval_request: Mapped['ApprovalRequests'] = relationship('ApprovalRequests', back_populates='approval_request_history')
#     approval_role: Mapped['ApprovalRoles'] = relationship('ApprovalRoles', back_populates='approval_request_history')
#     approval_status: Mapped['ApprovalStatus'] = relationship('ApprovalStatus', back_populates='approval_request_history')
#     step: Mapped[Optional['ApprovalFlowSteps']] = relationship('ApprovalFlowSteps', back_populates='approval_request_history')


# class ApprovalRoleUsers(Base):
#     __tablename__ = 'approval_role_users'
#     __table_args__ = (
#         ForeignKeyConstraint(['approval_role_id'], ['approval_roles.approval_role_id'], name='fk_approval_role_users_role'),
#         ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_approval_role_users_user'),
#         PrimaryKeyConstraint('approval_role_user_id', name='approval_role_users_pkey'),
#         Index('idx_approval_role_users_user_role', 'user_id', 'approval_role_id')
#     )

#     approval_role_user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     approval_role_id: Mapped[int] = mapped_column(Integer, nullable=False)
#     user_id: Mapped[int] = mapped_column(Integer, nullable=False)
#     active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

#     approval_role: Mapped['ApprovalRoles'] = relationship('ApprovalRoles', back_populates='approval_role_users')
#     user: Mapped['Users'] = relationship('Users', back_populates='approval_role_users')


# class AuditMeetingsCommitteesDetail(Base):
#     __tablename__ = 'audit_meetings_committees_detail'
#     __table_args__ = (
#         ForeignKeyConstraint(['id_audit_meeting_committees'], ['audit_meetings_committees.id'], name='audit_meetings_committees_detail_id_audit_meeting_committees_fo'),
#         ForeignKeyConstraint(['id_state'], ['state_detail_audit_meetings_committees.id'], name='audit_meetings_committees_detail_id_state_foreign'),
#         PrimaryKeyConstraint('id', name='audit_meetings_committees_detail_pkey')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     id_audit_meeting_committees: Mapped[Optional[int]] = mapped_column(BigInteger)
#     reference_number: Mapped[Optional[str]] = mapped_column(Text)
#     description_finding: Mapped[Optional[str]] = mapped_column(Text)
#     responsible_entity: Mapped[Optional[str]] = mapped_column(Text)
#     responsible_professional: Mapped[Optional[str]] = mapped_column(Text)
#     id_state: Mapped[Optional[int]] = mapped_column(BigInteger)
#     followup: Mapped[Optional[str]] = mapped_column(Text)
#     due_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     last_followup_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     audit_topic: Mapped[Optional[str]] = mapped_column(Text)
#     auditee_response: Mapped[Optional[str]] = mapped_column(Text)
#     auditor_analysis: Mapped[Optional[str]] = mapped_column(Text)
#     finding_code: Mapped[Optional[str]] = mapped_column(Text)
#     effect: Mapped[Optional[str]] = mapped_column(Text)
#     rate: Mapped[Optional[str]] = mapped_column(Text)
#     action_plan: Mapped[Optional[str]] = mapped_column(Text)
#     scheduled_date_action_plan_implementation: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     responsible: Mapped[Optional[str]] = mapped_column(Text)
#     action_plan_implementation_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

#     audit_meetings_committees: Mapped[Optional['AuditMeetingsCommittees']] = relationship('AuditMeetingsCommittees', back_populates='audit_meetings_committees_detail')
#     state_detail_audit_meetings_committees: Mapped[Optional['StateDetailAuditMeetingsCommittees']] = relationship('StateDetailAuditMeetingsCommittees', back_populates='audit_meetings_committees_detail')


# class ContractLine(Base):
#     __tablename__ = 'contract_line'
#     __table_args__ = (
#         ForeignKeyConstraint(['contract_id'], ['contracts.id'], name='contract_line_contract_id_foreign'),
#         ForeignKeyConstraint(['line_id'], ['lines.id'], name='contract_line_line_id_foreign'),
#         PrimaryKeyConstraint('id', name='contract_line_pkey')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     description: Mapped[str] = mapped_column(Text, nullable=False)
#     settle_value: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     accomplished_value: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("'0'::bigint"))
#     is_currency_usd: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
#     line_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     contract_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

#     contract: Mapped['Contracts'] = relationship('Contracts', back_populates='contract_line')
#     line: Mapped['Lines'] = relationship('Lines', back_populates='contract_line')


# class DisbursementProducts(Base):
#     __tablename__ = 'disbursement_products'
#     __table_args__ = (
#         ForeignKeyConstraint(['disbursement_id'], ['disbursement.id'], name='fk_disbursement'),
#         ForeignKeyConstraint(['product_id'], ['agreements_products.id'], name='fk_disbursement_product'),
#         PrimaryKeyConstraint('id', name='disbursement_products_pkey')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     disbursement_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     product_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

#     disbursement: Mapped['Disbursement'] = relationship('Disbursement', back_populates='disbursement_products')
#     product: Mapped['AgreementsProducts'] = relationship('AgreementsProducts', back_populates='disbursement_products')


# class MovementsPads(Base):
#     __tablename__ = 'movements_pads'
#     __table_args__ = (
#         CheckConstraint("operation::text = ANY (ARRAY['+'::character varying, '-'::character varying]::text[])", name='movements_pads_operation_check'),
#         ForeignKeyConstraint(['destination_line'], ['acquisitions.id'], ondelete='RESTRICT', onupdate='CASCADE', name='movements_pads_destination_line_foreign'),
#         ForeignKeyConstraint(['origin_line'], ['acquisitions.id'], ondelete='RESTRICT', onupdate='CASCADE', name='movements_pads_origin_line_foreign'),
#         PrimaryKeyConstraint('id', name='movements_pads_pkey')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     operation: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'+'::character varying"))
#     quantity_to_assign: Mapped[decimal.Decimal] = mapped_column(Numeric(20, 2), nullable=False)
#     origin_line: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     destination_line: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     observation: Mapped[Optional[str]] = mapped_column(Text)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     movement_group: Mapped[Optional[str]] = mapped_column(String(255))
#     system_observation: Mapped[Optional[str]] = mapped_column(String(255))
#     movement_type: Mapped[Optional[str]] = mapped_column(String(255))

#     acquisitions: Mapped['Acquisitions'] = relationship('Acquisitions', foreign_keys=[destination_line], back_populates='movements_pads_destination_line')
#     acquisitions_: Mapped['Acquisitions'] = relationship('Acquisitions', foreign_keys=[origin_line], back_populates='movements_pads_origin_line')


# class Notes(Base):
#     __tablename__ = 'notes'
#     __table_args__ = (
#         ForeignKeyConstraint(['acquisition_id'], ['acquisitions.id'], name='notes_acquisition_id_foreign'),
#         PrimaryKeyConstraint('id', name='notes_pkey')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
#     is_objection: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
#     acquisition_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     annotated_at: Mapped[Optional[str]] = mapped_column(Text)
#     description: Mapped[Optional[str]] = mapped_column(CITEXT)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))

#     acquisition: Mapped['Acquisitions'] = relationship('Acquisitions', back_populates='notes')


# class Notifications(Base):
#     __tablename__ = 'notifications'
#     __table_args__ = (
#         ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='notifications_user_id_foreign'),
#         PrimaryKeyConstraint('id', name='notifications_pkey')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     titulo: Mapped[str] = mapped_column(String(255), nullable=False)
#     mensaje: Mapped[str] = mapped_column(Text, nullable=False)
#     type: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'info'::character varying"))
#     is_read: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
#     data: Mapped[Optional[dict]] = mapped_column(JSON)
#     read_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

#     user: Mapped['Users'] = relationship('Users', back_populates='notifications')


# class Tasks(Base):
#     __tablename__ = 'tasks'
#     __table_args__ = (
#         ForeignKeyConstraint(['applicant_id'], ['users.id'], ondelete='SET NULL', onupdate='CASCADE', name='tasks_applicant_id_foreign'),
#         ForeignKeyConstraint(['executor_id'], ['users.id'], ondelete='SET NULL', onupdate='CASCADE', name='tasks_executor_id_foreign'),
#         ForeignKeyConstraint(['priority_id'], ['priorities.id'], ondelete='RESTRICT', onupdate='CASCADE', name='tasks_priority_id_foreign'),
#         ForeignKeyConstraint(['responsible_id'], ['users.id'], ondelete='SET NULL', onupdate='CASCADE', name='tasks_responsible_id_foreign'),
#         ForeignKeyConstraint(['reviewer_id'], ['users.id'], ondelete='SET NULL', onupdate='CASCADE', name='tasks_reviewer_id_foreign'),
#         ForeignKeyConstraint(['state_id'], ['task_states.id'], ondelete='SET NULL', onupdate='CASCADE', name='tasks_state_id_foreign'),
#         PrimaryKeyConstraint('id', name='tasks_pkey'),
#         Index('tasks_priority_id_index', 'priority_id')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     description: Mapped[str] = mapped_column(Text, nullable=False)
#     applicant_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     executor_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     responsible_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     state_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     request_types_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     reviewer_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     expected_fulfillment_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     execution_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     approval_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     file_path: Mapped[Optional[str]] = mapped_column(Text)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     name: Mapped[Optional[str]] = mapped_column(String(255))
#     priority_id: Mapped[Optional[int]] = mapped_column(BigInteger)

#     applicant: Mapped['Users'] = relationship('Users', foreign_keys=[applicant_id], back_populates='tasks_applicant')
#     executor: Mapped['Users'] = relationship('Users', foreign_keys=[executor_id], back_populates='tasks_executor')
#     priority: Mapped[Optional['Priorities']] = relationship('Priorities', back_populates='tasks')
#     responsible: Mapped['Users'] = relationship('Users', foreign_keys=[responsible_id], back_populates='tasks_responsible')
#     reviewer: Mapped[Optional['Users']] = relationship('Users', foreign_keys=[reviewer_id], back_populates='tasks_reviewer')
#     state: Mapped['TaskStates'] = relationship('TaskStates', back_populates='tasks')
#     observations: Mapped[list['Observations']] = relationship('Observations', back_populates='tasks')


# class TravelRequests(Base):
#     __tablename__ = 'travel_requests'
#     __table_args__ = (
#         ForeignKeyConstraint(['activity_id'], ['activities.id'], name='travel_requests_activities_fkey'),
#         ForeignKeyConstraint(['program_id'], ['programs.id'], name='travel_requests_program_id_fkey'),
#         ForeignKeyConstraint(['rubro_id'], ['rubros.id'], name='travel_requests_rubros_fkey'),
#         ForeignKeyConstraint(['travel_status_id'], ['travel_status.status_id'], name='travel_requests_travel_status_id_fkey'),
#         ForeignKeyConstraint(['traveler_user_id'], ['users.id'], name='travel_requests_traveler_user_id_fkey'),
#         PrimaryKeyConstraint('travel_request_id', name='travel_requests_pkey')
#     )

#     travel_request_id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     guid: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
#     code: Mapped[Optional[str]] = mapped_column(Text)
#     traveler_user_id: Mapped[Optional[int]] = mapped_column(Integer)
#     travel_start_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     travel_end_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     activity_purpose: Mapped[Optional[str]] = mapped_column(Text)
#     created_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
#     updated_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
#     account_number: Mapped[Optional[str]] = mapped_column(Text)
#     account_type_id: Mapped[Optional[int]] = mapped_column(Integer)
#     bank_id: Mapped[Optional[int]] = mapped_column(Integer)
#     expense_report_submission_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     cancelled_at: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     cancellation_reason: Mapped[Optional[str]] = mapped_column(Text)
#     cancelled_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
#     is_cancelled: Mapped[Optional[bool]] = mapped_column(Boolean)
#     request_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     requires_advance_payment: Mapped[Optional[bool]] = mapped_column(Boolean)
#     is_workshop_related: Mapped[Optional[bool]] = mapped_column(Boolean)
#     workshop_id: Mapped[Optional[int]] = mapped_column(Integer)
#     travel_category_id: Mapped[Optional[int]] = mapped_column(Integer)
#     total_hours: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))
#     total_days: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))
#     travel_status_id: Mapped[Optional[int]] = mapped_column(Integer)
#     location_report: Mapped[Optional[str]] = mapped_column(Text)
#     participating_institutions: Mapped[Optional[str]] = mapped_column(Text)
#     topics_discussed: Mapped[Optional[str]] = mapped_column(Text)
#     commitments: Mapped[Optional[str]] = mapped_column(Text)
#     report_comments: Mapped[Optional[str]] = mapped_column(Text)
#     approval_request_id: Mapped[Optional[int]] = mapped_column(Integer)
#     is_guest: Mapped[Optional[bool]] = mapped_column(Boolean)
#     guest_name: Mapped[Optional[str]] = mapped_column(Text)
#     guest_document: Mapped[Optional[str]] = mapped_column(Text)
#     guest_phone: Mapped[Optional[str]] = mapped_column(Text)
#     guest_email: Mapped[Optional[str]] = mapped_column(Text)
#     expense_approval_request_id: Mapped[Optional[int]] = mapped_column(Integer)
#     requires_tickets: Mapped[Optional[bool]] = mapped_column(Boolean)
#     is_international: Mapped[Optional[bool]] = mapped_column(Boolean)
#     country: Mapped[Optional[str]] = mapped_column(Text)
#     start_time: Mapped[Optional[str]] = mapped_column(Text)
#     end_time: Mapped[Optional[str]] = mapped_column(Text)
#     travel_type: Mapped[Optional[str]] = mapped_column(CHAR(1), comment='A = Air Travel, T = Ground Travel')
#     traveler_birth_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     supervisor_user_id: Mapped[Optional[int]] = mapped_column(Integer)
#     supervisor_approval_role_id: Mapped[Optional[int]] = mapped_column(Integer)
#     passport_support_document: Mapped[Optional[str]] = mapped_column(Text)
#     passport_support_path: Mapped[Optional[str]] = mapped_column(Text)
#     medical_assistance_document: Mapped[Optional[str]] = mapped_column(Text)
#     medical_assistance_path: Mapped[Optional[str]] = mapped_column(Text)
#     budget_item_id: Mapped[Optional[int]] = mapped_column(Integer)
#     current_request_order: Mapped[Optional[int]] = mapped_column(Integer)
#     supervisor_approved: Mapped[Optional[bool]] = mapped_column(Boolean)
#     additional_comments: Mapped[Optional[str]] = mapped_column(Text)
#     mentions_json: Mapped[Optional[str]] = mapped_column(Text)
#     mentioned_user_ids: Mapped[Optional[list[int]]] = mapped_column(ARRAY(Integer()))
#     advance_payment_rejected: Mapped[Optional[bool]] = mapped_column(Boolean)
#     report_support_document: Mapped[Optional[str]] = mapped_column(Text)
#     report_support_path: Mapped[Optional[str]] = mapped_column(Text)
#     region_id: Mapped[Optional[int]] = mapped_column(Integer)
#     invoice_reconciliation_required: Mapped[Optional[bool]] = mapped_column(Boolean)
#     program_id: Mapped[Optional[int]] = mapped_column(Integer)
#     advance_amount: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))
#     rubro_id: Mapped[Optional[int]] = mapped_column(Integer)
#     short_rubro: Mapped[Optional[str]] = mapped_column(Text)
#     year_rubro: Mapped[Optional[int]] = mapped_column(Integer)
#     activity_id: Mapped[Optional[int]] = mapped_column(Integer)

#     activity: Mapped[Optional['Activities']] = relationship('Activities', back_populates='travel_requests')
#     program: Mapped[Optional['Programs']] = relationship('Programs', back_populates='travel_requests')
#     rubro: Mapped[Optional['Rubros']] = relationship('Rubros', back_populates='travel_requests')
#     travel_status: Mapped[Optional['TravelStatus']] = relationship('TravelStatus', back_populates='travel_requests')
#     traveler_user: Mapped[Optional['Users']] = relationship('Users', back_populates='travel_requests')
#     travel_accommodations: Mapped[list['TravelAccommodations']] = relationship('TravelAccommodations', back_populates='travel_request')
#     travel_itineraries: Mapped[list['TravelItineraries']] = relationship('TravelItineraries', back_populates='travel_request')


# class UsersPrograms(Base):
#     __tablename__ = 'users_programs'
#     __table_args__ = (
#         ForeignKeyConstraint(['program_id'], ['programs.id'], name='users_programs_id_program_fkey'),
#         ForeignKeyConstraint(['user_id'], ['users.id'], name='users_programs_id_user_fkey'),
#         PrimaryKeyConstraint('user_program_id', name='users_programs_pkey')
#     )

#     user_program_id: Mapped[int] = mapped_column(Integer, Sequence('users_programs_id_usuario_programa_seq'), primary_key=True)
#     program_id: Mapped[int] = mapped_column(Integer, nullable=False)
#     user_id: Mapped[int] = mapped_column(Integer, nullable=False)

#     program: Mapped['Programs'] = relationship('Programs', back_populates='users_programs')
#     user: Mapped['Users'] = relationship('Users', back_populates='users_programs')


# class Observations(Base):
#     __tablename__ = 'observations'
#     __table_args__ = (
#         ForeignKeyConstraint(['id_task'], ['tasks.id'], ondelete='SET NULL', onupdate='CASCADE', name='observations_id_task_foreign'),
#         ForeignKeyConstraint(['id_user'], ['users.id'], ondelete='SET NULL', onupdate='CASCADE', name='observations_id_user_foreign'),
#         PrimaryKeyConstraint('id', name='observations_pkey')
#     )

#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     observation: Mapped[str] = mapped_column(Text, nullable=False)
#     id_task: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     id_user: Mapped[int] = mapped_column(BigInteger, nullable=False)
#     created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
#     updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

#     tasks: Mapped['Tasks'] = relationship('Tasks', back_populates='observations')
#     users: Mapped['Users'] = relationship('Users', back_populates='observations')


# class TravelAccommodations(Base):
#     __tablename__ = 'travel_accommodations'
#     __table_args__ = (
#         ForeignKeyConstraint(['municipality_id'], ['regions.id'], name='travel_accommodations_municipality_id_fkey'),
#         ForeignKeyConstraint(['travel_request_id'], ['travel_requests.travel_request_id'], name='fk_travel_accommodation'),
#         PrimaryKeyConstraint('travel_accommodation_id', name='travel_accommodations_pkey')
#     )

#     travel_accommodation_id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     travel_request_id: Mapped[Optional[int]] = mapped_column(Integer)
#     municipality_id: Mapped[Optional[int]] = mapped_column(Integer)
#     comments: Mapped[Optional[str]] = mapped_column(Text)
#     check_in_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     check_out_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     accommodation_type: Mapped[Optional[str]] = mapped_column(Text, comment='RZ = Rural Area, C = City')
#     support_document: Mapped[Optional[str]] = mapped_column(Text)
#     support_document_path: Mapped[Optional[str]] = mapped_column(Text)
#     foundation_managed_payment: Mapped[Optional[bool]] = mapped_column(Boolean)
#     project_id: Mapped[Optional[int]] = mapped_column(Integer)
#     budget_item_id: Mapped[Optional[int]] = mapped_column(Integer)

#     municipality: Mapped[Optional['Regions']] = relationship('Regions', back_populates='travel_accommodations')
#     travel_request: Mapped[Optional['TravelRequests']] = relationship('TravelRequests', back_populates='travel_accommodations')


# class TravelItineraries(Base):
#     __tablename__ = 'travel_itineraries'
#     __table_args__ = (
#         ForeignKeyConstraint(['destination_municipality_id'], ['regions.id'], name='fk_travel_destination'),
#         ForeignKeyConstraint(['origin_municipality_id'], ['regions.id'], name='fk_travel_origin'),
#         ForeignKeyConstraint(['travel_request_id'], ['travel_requests.travel_request_id'], name='fk_travel_itinerary'),
#         PrimaryKeyConstraint('travel_itinerary_id', name='travel_itineraries_pkey')
#     )

#     travel_itinerary_id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     travel_request_id: Mapped[int] = mapped_column(Integer, nullable=False)
#     travel_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
#     destination_municipality_id: Mapped[Optional[int]] = mapped_column(Integer)
#     origin_municipality_id: Mapped[Optional[int]] = mapped_column(Integer)
#     departure_time: Mapped[Optional[str]] = mapped_column(Text)
#     comments: Mapped[Optional[str]] = mapped_column(Text)
#     origin_village: Mapped[Optional[str]] = mapped_column(Text)
#     destination_village: Mapped[Optional[str]] = mapped_column(Text)
#     is_destination_village: Mapped[Optional[bool]] = mapped_column(Boolean)
#     is_origin_village: Mapped[Optional[bool]] = mapped_column(Boolean)
#     boarding_pass_path: Mapped[Optional[str]] = mapped_column(Text)
#     boarding_pass_document: Mapped[Optional[str]] = mapped_column(Text)
#     is_rural_area: Mapped[Optional[bool]] = mapped_column(Boolean)
#     rural_area_comments: Mapped[Optional[str]] = mapped_column(Text)
#     ticket_support_document: Mapped[Optional[str]] = mapped_column(Text)
#     ticket_support_path: Mapped[Optional[str]] = mapped_column(Text)
#     requires_air_tickets: Mapped[Optional[bool]] = mapped_column(Boolean)
#     project_id: Mapped[Optional[int]] = mapped_column(Integer)
#     budget_item_id: Mapped[Optional[int]] = mapped_column(Integer)

#     destination_municipality: Mapped[Optional['Regions']] = relationship('Regions', foreign_keys=[destination_municipality_id], back_populates='travel_itineraries_destination_municipality')
#     origin_municipality: Mapped[Optional['Regions']] = relationship('Regions', foreign_keys=[origin_municipality_id], back_populates='travel_itineraries_origin_municipality')
#     travel_request: Mapped['TravelRequests'] = relationship('TravelRequests', back_populates='travel_itineraries')
