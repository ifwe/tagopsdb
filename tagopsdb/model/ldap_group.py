from sqlalchemy.dialects.mysql import INTEGER

from .meta import Base, Column, String


class LdapGroup(Base):
    __tablename__ = 'ldap_groups'

    gid = Column(INTEGER(unsigned=True), primary_key=True)
    group_name = Column(String(50), nullable=False, unique=True)
