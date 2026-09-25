

agreement: Mapped[Optional['Agreements']] = relationship('Agreements', back_populates='agreement_implementers'
)