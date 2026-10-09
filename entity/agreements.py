import datetime
from typing import Optional

from sqlalchemy import BigInteger, Boolean, Date, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base
from sqlalchemy.dialects.postgresql import CITEXT, TIMESTAMP
from entity.agreement_origins   import AgreementOrigins
from entity.agreement_stages    import AgreementStages
from entity.agreement_types     import AgreementTypes
from entity.modalities          import Modalities
from entity.pillars             import Pillars
from entity.programs            import Programs
from entity.regions            import Regions

import decimal

class Agreements(Base):
    __tablename__ = 'agreements'
    __table_args__ = (
        ForeignKeyConstraint(['agreement_id'], ['agreements.id'], name='agreements_agreement_id_foreign'),
        ForeignKeyConstraint(['agreement_stage_id'], ['agreement_stages.id'], name='agreements_agreement_stage_id_foreign'),
        ForeignKeyConstraint(['agreement_origin_id'], ['agreement_origins.id'], name='agreements_agreement_origin_id_foreign'),
        ForeignKeyConstraint(['agreement_type_id'], ['agreement_types.id'], name='agreements_agreement_type_id_foreign'),
        ForeignKeyConstraint(['modality_id'], ['modalities.id'], name='agreements_modality_id_foreign'),
        ForeignKeyConstraint(['pillar_id'], ['pillars.id'], name='agreements_pillar_id_foreign'),
        ForeignKeyConstraint(['program_id'], ['programs.id'], name='agreements_program_id_foreign'),
        ForeignKeyConstraint(['region_id'], ['regions.id'], name='agreements_region_id_foreign'),
        PrimaryKeyConstraint('id', name='agreements_pkey')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(CITEXT)
    code: Mapped[Optional[str]] = mapped_column(String(255))
    local: Mapped[Optional[int]] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(CITEXT)
    value: Mapped[Optional[int]] = mapped_column(BigInteger)
    is_currency_usd: Mapped[bool] = mapped_column(Boolean, nullable=False)
    year: Mapped[Optional[int]] = mapped_column(Integer)
    request_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    finish_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    signature_fpn: Mapped[Optional[datetime.date]] = mapped_column(Date)
    signature_ei: Mapped[Optional[datetime.date]] = mapped_column(Date)
    file_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    policy_approval: Mapped[bool] = mapped_column(Boolean, nullable=False)
    signature_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    time_limit: Mapped[Optional[str]] = mapped_column(String(255))
    policy_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    liquidation_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    final_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    # Llaves foráneas
    agreement_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    program_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    pillar_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    agreement_type_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    agreement_stage_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    agreement_origin_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    region_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    modality_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    marking: Mapped[Optional[str]] = mapped_column(String(255))
    priority: Mapped[Optional[str]] = mapped_column(String(255))
    notes: Mapped[Optional[str]] = mapped_column(Text)
    is_valid: Mapped[Optional[bool]] = mapped_column(Boolean)
    observations: Mapped[Optional[str]] = mapped_column(Text)
    products: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    alert: Mapped[Optional[str]] = mapped_column(String(255))
    liquidation_file_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    finish_file_record_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    general_remarks: Mapped[Optional[str]] = mapped_column(Text)
    email_notifications: Mapped[Optional[str]] = mapped_column(String(255))
    executed_value: Mapped[Optional[int]] = mapped_column(BigInteger)
    financial_progress: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    summary: Mapped[Optional[str]] = mapped_column(String(255))
    total_value: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    financial_cutoff_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    value_executes_fpn: Mapped[Optional[int]] = mapped_column(BigInteger)
    value_executes_entity: Mapped[Optional[int]] = mapped_column(BigInteger)
    counterpart_execution_progress: Mapped[Optional[int]] = mapped_column(BigInteger)
    ei_executed_value: Mapped[Optional[int]] = mapped_column(BigInteger)
    fpn_executed_value: Mapped[Optional[int]] = mapped_column(BigInteger)
    total_value_executes_FPN: Mapped[Optional[int]] = mapped_column('total_value_executes_FPN', BigInteger)
    total_value_executes_EI: Mapped[Optional[int]] = mapped_column('total_value_executes_EI', BigInteger)
    last_report_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    contract_file_sharepoint: Mapped[Optional[str]] = mapped_column(Text)
    shared_ei_one_drive: Mapped[Optional[str]] = mapped_column(Text)
    shared_products_ei_one_drive: Mapped[Optional[str]] = mapped_column(Text)
    village: Mapped[Optional[str]] = mapped_column(String(255))
    hectares: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    beneficiaries: Mapped[Optional[int]] = mapped_column(Integer)
    advance_hectares: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    advance_beneficiaries: Mapped[Optional[int]] = mapped_column(Integer)
    hectares_beneficiaries_updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=6))
    have_aatis: Mapped[Optional[bool]] = mapped_column(Boolean)
    aatis: Mapped[Optional[str]] = mapped_column(Text)
    councils: Mapped[Optional[str]] = mapped_column(Text)
    resguard: Mapped[Optional[str]] = mapped_column(Text)
    municipality: Mapped[Optional[str]] = mapped_column(Text)
    department: Mapped[Optional[str]] = mapped_column(Text)
    legal_observations: Mapped[Optional[str]] = mapped_column(Text)
    acquisitions_observations: Mapped[Optional[str]] = mapped_column(Text)
    uer_observations: Mapped[Optional[str]] = mapped_column(Text)



    # Relaciones
    agreement_parent: Mapped[Optional['Agreements']] = relationship('Agreements', remote_side=[id])
    agreement_origin: Mapped['AgreementOrigins'] = relationship('AgreementOrigins')
    agreement_stage: Mapped['AgreementStages'] = relationship('AgreementStages')
    agreement_type: Mapped['AgreementTypes'] = relationship('AgreementTypes')
    modality: Mapped[Optional['Modalities']] = relationship('Modalities')
    pillar: Mapped[Optional['Pillars']] = relationship('Pillars')
    program: Mapped['Programs'] = relationship('Programs')
    region: Mapped[Optional['Regions']] = relationship('Regions')
