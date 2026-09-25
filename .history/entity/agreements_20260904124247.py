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
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

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
    

    
    
    
   
   
   
   
   
    

    user: Mapped[Optional[Users]] = relationship('Users')
    travel_status: Mapped[Optional['TravelStatus']] = relationship('TravelStatus')
    activity: Mapped[Optional['Activities']] = relationship('Activities')
    rubro: Mapped[Optional['Rubros']] = relationship('Rubros')
    # travel_accommodations: Mapped[list['TravelAccommodations']] = relationship('TravelAccommodations', back_populates='travel_request')
    # travel_itineraries: Mapped[list['TravelItineraries']] = relationship('TravelItineraries', back_populates='travel_request')
