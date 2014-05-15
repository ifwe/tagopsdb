from .meta import Base, Column, String, SurrogatePK


class NagContact(SurrogatePK, Base):
    __tablename__ = 'nag_contacts'

    name = Column(String(length=32), nullable=False, unique=True)
    alias = Column(String(length=80))
    email = Column(String(length=80))
    pager = Column(String(length=80))
