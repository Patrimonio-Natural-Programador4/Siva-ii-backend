

# agreement: Mapped[Optional['Agreements']] = relationship('Agreements', back_populates='agreement_products')


# Descomentar cuando crees entity/agreement_products.py y entity/agreement_implementers.py:
    # agreement_products: Mapped[List['AgreementProducts']] = relationship('AgreementProducts', back_populates='agreement', cascade='all, delete-orphan')
    # agreement_implementers: Mapped[List['AgreementImplementers']] = relationship('AgreementImplementers', back_populates='agreement', cascade='all, delete-orphan')