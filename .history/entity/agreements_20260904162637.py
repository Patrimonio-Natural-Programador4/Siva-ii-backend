# =======================================================
# 1. COMPATIBILIDAD Y TIPADO ESTÁNDAR
# =======================================================
from __future__ import annotations
import datetime
import decimal
import uuid
from typing import Optional, List, Any

# ==============================================================================
# 2. TIPOS DE DATOS Y RESTRICCIONES DE BASE DE DATOS (SQLAlchemy Core)
# ==============================================================================
from sqlalchemy import ARRAY, DateTime, Integer, Date, Text, ForeignKeyConstraint, PrimaryKeyConstraint,  Uuid, Boolean, Numeric, CHAR, Sequence, text

# ====================================================
# 3. MAPEADOR OBJETO-RELACIONAL (SQLAlchemy ORM)
# ===================================================
from sqlalchemy.orm import BigInteger, DeclarativeBase, Mapped, mapped_column, relationship

# ==============================================================================
# 4. CONFIGURACIÓN DEL PROYECTO Y ENTIDADES RELACIONADAS (SIVA II Domain)
# ==============================================================================
from database.database import Base
from entity.modalities import Modalities
from entity.programs import Programs
from entity.regions import Regions
from entity.capacity_assessments import CapacityAssessments
from entity.pillars import Pillars
from entity.agreement_origins import AgreementOrigins
from entity.agreement_stages import AgreementStages
from entity.agreement_types import AgreementTypes

# ==============================================================================
# IDENTIFICACIÓN DE TABLA Y LLAVES FORÁNEAS FÍSICAS (PostgreSQL Constraints)
# ==============================================================================

class Agreements(Base):
    __tablename__ = 'agreements'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='agreements_pkey'),
        
        ForeignKeyConstraint(['agreement_id'], ['agreement.id'], name='agreements_agreement_id_fkey'),
        ForeignKeyConstraint(['agreement_origin_id'], ['agreement_origins.id'], name='agreements_agreement_origin_id_fkey'),
        ForeignKeyConstraint(['agreement_stage_id'], ['agreement_stages.id'], name='agreements_agreement_stage_id_fkey'),
        ForeignKeyConstraint(['agreement_type_id'], ['agreement_types.id'], name='agreements_agreement_type_id_fkey'),
        ForeignKeyConstraint(['modality_id'], ['modalities.id'], name='agreements_modality_id_fkey'),
        ForeignKeyConstraint(['pillar_id'], ['pillars.id'], name='agreements_pillar_id_fkey'),        
        ForeignKeyConstraint(['program_id'], ['programs.id'], name='agreements_program_id_fkey'),        
        ForeignKeyConstraint(['region_id'], ['regions.id'], name='agreements_region_id_fkey'),       
        ForeignKeyConstraint(['capacity_assessment_id'], ['capacity_assessments.id'], name='agreements_capacity_assessment_id_fkey')
    )
    
# ==============================================================================
# ATRIBUTOS Y COLUMNAS FÍSICAS DE LA TABLA (PostgreSQL Mapped Columns)
# ==============================================================================
 
 # Llave primaria y datos basicos
    id: Mapped[int] = mapped_column(Integer, primary_key=True)    
    name: Mapped[Optional[str]] = mapped_column(Text)    
    code: Mapped[Optional[str]] = mapped_column(Text)    
    local: Mapped[Optional[str]] = mapped_column(Text)    
    description: Mapped[Optional[str]] = mapped_column(Text)    
    value: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))    
    is_currency_usd: Mapped[Optional[bool]] = mapped_column(Boolean)    
    year: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Fechas y cronogramas    
    request_date: Mapped[Optional[datetime.date]] = mapped_column(Date)    
    finish_date: Mapped[Optional[datetime.date]] = mapped_column(Date)    
    signature_fpn: Mapped[Optional[datetime.date]] = mapped_column(Date)    
    signature_ei: Mapped[Optional[datetime.date]] = mapped_column(Date)    
    file_date: Mapped[Optional[datetime.date]] = mapped_column(Date)    
    policy_approval: Mapped[Optional[bool]] = mapped_column(Boolean)    
    signature_date: Mapped[Optional[datetime.date]] = mapped_column(Date)    
    time_limit: Mapped[Optional[str]] = mapped_column(Text)    
    policy_date: Mapped[Optional[datetime.date]] = mapped_column(Date)    
    final_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    liquidation_date: Mapped[Optional[datetime.date]] = mapped_column(Date)  
    finish_file_record_date: Mapped[Optional[datetime.date]] = mapped_column(Date)  
    financial_cutoff_date: Mapped[Optional[datetime.date]] = mapped_column(Date)    
    last_report_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    
    # Llaves foraneas
    agreement_id: Mapped[Optional[int]] = mapped_column(BigInteger)    
    program_id: Mapped[Optional[int]] = mapped_column(Integer)    
    pillar_id: Mapped[Optional[int]] = mapped_column(Integer)    
    agreement_type_id: Mapped[Optional[int]] = mapped_column(Integer)    
    agreement_stage_id: Mapped[Optional[int]] = mapped_column(Integer)    
    agreement_origin_id: Mapped[Optional[int]] = mapped_column(Integer)    
    region_id: Mapped[Optional[int]] = mapped_column(Integer)
    modality_id: Mapped[Optional[int]] = mapped_column(Integer)
    capacity_assessment_id: Mapped[Optional[int]] = mapped_column(Integer)
    
        
    # Estados y soportes
    marking: Mapped[Optional[str]] = mapped_column(Text)    
    priority: Mapped[Optional[str]] = mapped_column(Text)    
    notes: Mapped[Optional[str]] = mapped_column(Text)    
    is_valid: Mapped[Optional[bool]] = mapped_column(Boolean)    
    observations: Mapped[Optional[str]] = mapped_column(Text)    
    products: Mapped[Optional[str]] = mapped_column(Text)    
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))    
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))    
    alert: Mapped[Optional[str]] = mapped_column(Text)
    general_remarks: Mapped[Optional[str]] = mapped_column(Text)
    email_notifications: Mapped[Optional[str]] = mapped_column(Text)
    
    
    liquidation_file_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    
    shared_ei_one_drive: Mapped[Optional[str]] = mapped_column(Text)
    shared_products_ei_one_drive: Mapped[Optional[str]] = mapped_column(Text)
    
    
    #  ----  Control financiero
    executed_value: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))    
    financial_progress: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))    
    summary: Mapped[Optional[str]] = mapped_column(Text) # Buscar    
    total_value: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2)) 
    value_executes_fpn: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))
    value_executes_entity: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))
    counterpart_execution_progress: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))
    ei_executed_value: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))
    fpn_executed_value: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))
    total_value_executes_fpn: Mapped[Optional[decimal.Decimal]] = mapped_column('total_value_executes_FPN', Numeric(18, 2))
    total_value_executes_ei: Mapped[Optional[decimal.Decimal]] = mapped_column('total_value_executes_EI', Numeric(18, 2))
        
    # ---- Ubicacion territorial y metas fisicas
    village: Mapped[Optional[str]] = mapped_column(Text)    
    hectares: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))    
    beneficiaries: Mapped[Optional[int]] = mapped_column(Integer)    
    advance_hectares: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 2))    
    advance_beneficiaries: Mapped[Optional[int]] = mapped_column(Integer)    
    hectares_beneficiaries_updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))    
    have_aatis: Mapped[Optional[bool]] = mapped_column(Boolean)    
    aatis: Mapped[Optional[str]] = mapped_column(Text)    
    councils: Mapped[Optional[str]] = mapped_column(Text)    
    resguard: Mapped[Optional[str]] = mapped_column(Text)    
    municipality: Mapped[Optional[str]] = mapped_column(Text)    
    department: Mapped[Optional[str]] = mapped_column(Text)    
    
    
    
    # ==============================================================================
    # RELACIONES LÓGICAS Y NAVEGACIÓN ORM (SQLAlchemy Relationships)
    # ==============================================================================
 
    parent_agreement: Mapped[Optional['Agreements']] = relationship('Agreements', remote_side=[id], back_populates='child_agreements')
    child_agreements: Mapped[List['Agreements']] = relationship('Agreements', back_populates='parent_agreement')
 
    modality: Mapped[Optional[Modalities]] = relationship('Modalities')
    program: Mapped[Optional[Programs]] = relationship('Programs')
    region: Mapped[Optional[Regions]] = relationship('Regions')
    
    
    # Otras relaciones de la entidad:
    capacity_assessment: Mapped[Optional[CapacityAssessments]] = relationship('CapacityAssessments')
    agreement_origin: Mapped[Optional[AgreementOrigins]] = relationship('AgreementOrigins')
    agreement_stage: Mapped[Optional[AgreementStages]] = relationship('AgreementStages')
    agreement_type: Mapped[Optional[AgreementTypes]] = relationship('AgreementTypes')
    pillar: Mapped[Optional[Pillars]] = relationship('Pillars')
   
