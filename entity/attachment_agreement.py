from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from sqlalchemy import Integer, Text, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base

if TYPE_CHECKING:
    from entity.capacity_assessments import CapacityAssessments
    from entity.documents_types_agreements import DocumentsTypesAgreements



class Attachment_Agreement(Base):
    __tablename__ = 'attachment_agreement'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='attachment_agreement_pkey'),
        ForeignKeyConstraint(
            ['capacity_assessments_id'],
            ['capacity_assessments.id'],
            name='fk_attachment_agreements_capacity_assessments',
            ondelete='CASCADE'
        ),
        ForeignKeyConstraint(
            ['documents_types_agreements_id'],
            ['documents_types_agreements.id'],
            name='fk_attachment_agreements_documents_types_agreements',
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    attachment_name: Mapped[Optional[str]] = mapped_column(Text)
    path_document: Mapped[Optional[str]] = mapped_column(Text)
    capacity_assessments_id: Mapped[Optional[int]] = mapped_column(Integer)
    observations: Mapped[Optional[str]] = mapped_column(Text)
    documents_types_agreements_id: Mapped[Optional[int]] = mapped_column(Integer)


    # RELACIONES ORM
    
    capacity_assessments: Mapped[Optional['CapacityAssessments']] = relationship('CapacityAssessments', back_populates='AttachmentAgreementCapacityAssessments')
    documents_types_agreements: Mapped[Optional['DocumentsTypesAgreements']] = relationship('DocumentsTypesAgreements', back_populates='AttachmentAgreementDocumentsTypesAgreements')
        
    
    
    
    
    