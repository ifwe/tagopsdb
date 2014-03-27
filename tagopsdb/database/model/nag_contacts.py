from sqlalchemy import Column, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from .base import Base


class NagContacts(Base):
    __tablename__ = 'nag_contacts'

    id = Column(INTEGER(), primary_key=True)
    name = Column(VARCHAR(length=32), nullable=False, unique=True)
    alias = Column(VARCHAR(length=80))
    email = Column(VARCHAR(length=80))
    pager = Column(VARCHAR(length=80))
