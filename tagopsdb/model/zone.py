from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class Zone(Base):
    __tablename__ = 'zones'

    id = Column(u'ZoneID', INTEGER(), primary_key=True)
    zone_name = Column(u'zoneName',String(length=30))
    mx_priority = Column(u'mxPriority', INTEGER())
    mx_host_id = Column(u'mxHostID', String(length=30))
    ns_priority = Column(u'nsPriority', INTEGER())
    nameserver = Column(String(length=30))
    cnames = relationship('Cname', backref='zone')
