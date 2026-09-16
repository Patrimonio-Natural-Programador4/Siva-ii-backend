from __future__ import annotations
from typing import Optional, List
from sqlalchemy import Integer, Numeric, Text, ForeignKeyConstraint, PrimaryKeyConstraint, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from database.database import Base
from sqlalchemy import text
from sqlalchemy.orm import mapped_column, Mapped

from sqlalchemy import Column, Integer, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class VwMenu(Base):
    __tablename__ = 'vw_menu'

    menu_id = Column(Integer, primary_key=True)
    name = Column(Text)
    parent_menu_id = Column(Integer)
    order_menu = Column(Integer)
    module_id = Column(Integer)
    icon = Column(Text)
    url = Column(Text)
    parent_value = Column(Text)
    parent_order = Column(Integer)
    role_id = Column(Integer)
    parent_icon = Column(Text)
    parent_url = Column(Text)
    __mapper_args__ = { 
        'primary_key': [menu_id]
    }

    @classmethod
    def __declare_last__(cls):
        #  Evitar que se pueda hacer commit en esta clase (solo lectura). 
        pass  