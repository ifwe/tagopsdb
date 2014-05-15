from sqlalchemy.orm import relationship

from .meta import Base, Column, String, SurrogatePK


class NagContactGroup(SurrogatePK, Base):
    __tablename__ = 'nag_contact_groups'

    name = Column(String(length=32), nullable=False, unique=True)
    alias = Column(String(length=80))
    nag_contacts = relationship(
        'NagContact',
        secondary='nag_contact_groups_members',
        backref='nag_contact_groups'
    )