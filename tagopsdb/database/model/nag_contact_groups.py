from sqlalchemy import Column, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import relationship

from .base import Base


class NagContactGroups(Base):
    __tablename__ = 'nag_contact_groups'

    id = Column(INTEGER(), primary_key=True)
    name = Column(VARCHAR(length=32), nullable=False, unique=True)
    alias = Column(VARCHAR(length=80))
    nag_contacts = relationship(
        'NagContacts',
        secondary='nag_contact_groups_members',
        backref='nag_contact_groups'
    )
