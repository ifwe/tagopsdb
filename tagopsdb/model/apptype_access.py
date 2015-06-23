from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT

from .meta import Base, Column


class ApptypeAccess(Base):
    __tablename__ = 'apptype_access'
    
    environment_id = Column(
        INTEGER(),
        ForeignKey('environments.environmentID', ondelete='cascade'),
        primary_key=True
    )
    app_id = Column(
        SMALLINT(),
        ForeignKey('app_definitions.AppID', ondelete='cascade'),
        primary_key=True
    )
    gid = Column(
        INTEGER(unsigned=True),
        ForeignKey('ldap_groups.gid', ondelete='cascade'),
        primary_key=True
    )
